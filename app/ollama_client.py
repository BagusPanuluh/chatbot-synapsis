import httpx
import os

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://host.docker.internal:11434')
MODEL = os.getenv('OLLAMA_MODEL', 'llama3.2:3b')

async def generate_reply(prompt: str) -> str:
    """Call local Ollama HTTP API /api/generate to get model reply.
    Simple implementation using httpx (async).
    """
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 256,
        "temperature": 0.2
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns `choices` with `content` (may differ based on version)
        # We try to extract sensible content.
        if 'choices' in data and len(data['choices'])>0:
            # join text parts
            contents = []
            for ch in data['choices']:
                if isinstance(ch.get('message'), dict):
                    contents.append(ch['message'].get('content',''))
                else:
                    contents.append(ch.get('content',''))
            return '\n'.join(contents).strip()
        # fallback: raw text
        return data.get('text', '').strip()