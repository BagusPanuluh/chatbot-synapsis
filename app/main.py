from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.db import (
    init_db, save_message, get_last_n_messages,
    save_order_example, get_order_by_id,
    save_products_example, get_product_by_name, get_all_products
)
from app.ollama_client import generate_reply
from app.tools import call_order_status_tool, call_product_info_tool
import os

app = FastAPI(title="Synapsis Chatbot")

# init database (creates sqlite file if not exists)
init_db()
# insert example order (id=1001) if not exists
save_order_example()
# insert example products
save_products_example()


class ChatRequest(BaseModel):
    user_id: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    tool_called: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = None


@app.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    # save user message
    save_message(req.user_id, 'user', req.message)

    tool_called = None
    lower = req.message.lower()

    if 'pesanan' in lower:
        # coba ambil order_id
        order_id = None
        if req.metadata and 'order_id' in req.metadata:
            order_id = req.metadata['order_id']
        else:
            import re
            m = re.search(r"(\d{3,})", req.message)
            if m:
                order_id = int(m.group(1))
        tool_called = 'order_status'
        bot_reply = call_order_status_tool(order_id, req.message)

    elif 'produk apa saja' in lower or 'daftar produk' in lower or 'list produk' in lower:
        tool_called = 'product_list'
        products = get_all_products()
        if products:
            names = ', '.join([p['name'] for p in products])
            bot_reply = f"Produk yang tersedia di toko ini: {names}."
        else:
            bot_reply = "Saat ini tidak ada produk yang tersedia."

    elif 'produk' in lower or 'kelebihan' in lower or 'informasi produk' in lower:
        # coba ambil nama produk setelah kata 'produk'
        import re
        m = re.search(r"produk ([a-zA-Z0-9]+)", lower)
        product_name = m.group(1) if m else None
        tool_called = 'product_info'
        bot_reply = call_product_info_tool(product_name)

    elif 'garansi' in lower:
        tool_called = 'warranty_info'
        bot_reply = (
            "Semua produk di toko ini bergaransi resmi 1 tahun. "
            "Klaim garansi bisa dilakukan dengan membawa nota pembelian ke service center resmi."
        )

    else:
        # kalau bukan tool, pakai LLM
        context = get_last_n_messages(req.user_id, n=3)
        prompt = """
You are a helpful customer support assistant for an online shop. Use the conversation history and the user's message to reply concisely in Indonesian.

Conversation history:
{history}

User: {user_message}
Assistant:
""".format(
            history='\n'.join([f"{m['role']}: {m['content']}" for m in context]),
            user_message=req.message
        )

        try:
            bot_reply = await generate_reply(prompt)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM error: {e}")

    # save bot reply
    save_message(req.user_id, 'assistant', bot_reply)

    # return history (last 10 messages)
    conversation_history = get_last_n_messages(req.user_id, n=10)

    return ChatResponse(reply=bot_reply, tool_called=tool_called, conversation_history=conversation_history)


@app.get('/orders/{order_id}')
async def get_order(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    return order


@app.get('/products/{name}')
async def get_product(name: str):
    product = get_product_by_name(name)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product


@app.get('/products')
async def list_products():
    products = get_all_products()
    return products


@app.get('/')
def root():
    return {"status": "ok", "info": "Synapsis Chatbot API"}
