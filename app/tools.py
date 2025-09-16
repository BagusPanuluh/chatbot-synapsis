from app.db import get_order_by_id, get_product_by_name

def call_order_status_tool(order_id: int | None) -> str:
    if order_id is None:
        return "Bisa berikan nomor pesanan Anda (contoh: 1001)?"
    order = get_order_by_id(order_id)
    if not order:
        return f"Mohon maaf, saya tidak menemukan pesanan dengan nomor {order_id}."
    return (f"Pesanan {order['id']} status: {order['status']}. "
            f"Ekspedisi: {order['shipping_provider']}. ETA: {order['eta']}")

def call_product_info_tool(product_name: str | None) -> str:
    if not product_name:
        return "Produk apa yang ingin Anda ketahui informasinya?"
    product = get_product_by_name(product_name)
    if not product:
        return f"Mohon maaf, saya tidak menemukan produk dengan nama {product_name}."
    return f"{product['name']}: {product['description']}"