import httpx
import os
import json
import platform
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
ARIA_NAME = os.getenv("ARIA_NAME", "Aria")


def get_system_message() -> dict:
    now = datetime.now()
    os_name = platform.system()
    os_version = platform.version()

    content = f"""You are {ARIA_NAME}, a local AI assistant running on the user's computer. Forget any previous identity — you are NOT Qwen, NOT ChatGPT, NOT any other AI. You are {ARIA_NAME}.

Your personality: helpful, casual, slightly witty — like a smart friend. Skip filler phrases like "Certainly!" or "Of course!". Be direct and concise.

Your capabilities: chat, write/debug code, execute shell commands on Windows, monitor system resources, remember conversation history.

Current context:
- Time: {now.strftime("%A, %d %B %Y %H:%M")}
- OS: {os_name} {os_version}
- Model: {OLLAMA_MODEL}
- Everything runs locally, no cloud, no internet access

Rules:
- Always respond in the same language the user writes in
- Never claim you can browse the internet
- If unsure, say so — never make things up
- For shell commands, explain what it does first"""

    return {"role": "user", "content": content}


def get_system_ack() -> dict:
    return {
        "role": "assistant",
        "content": f"Understood. I'm {ARIA_NAME}, your local AI assistant. Ready to help!",
    }


async def chat(messages: list[dict]) -> str:
    full_messages = [get_system_message(), get_system_ack()] + messages
    payload = {
        "model": OLLAMA_MODEL,
        "messages": full_messages,
        "stream": False,
        "keep_alive": 0,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]


async def chat_stream(messages: list[dict]):
    full_messages = [get_system_message(), get_system_ack()] + messages
    payload = {
        "model": OLLAMA_MODEL,
        "messages": full_messages,
        "stream": True,
        "keep_alive": 0,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST", f"{OLLAMA_BASE_URL}/api/chat", json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if data.get("done"):
                        break
                except json.JSONDecodeError:
                    continue


async def generate_title(message: str) -> str:
    prompt = f"""Generate a short chat title (3-5 words max) for a conversation that starts with this message.
Reply with ONLY the title, no quotes, no punctuation at the end.

Message: {message}
Title:"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "keep_alive": 0,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        title = data["message"]["content"].strip()
        return title[:40] if len(title) > 40 else title


async def is_ollama_running() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return response.status_code == 200
    except Exception:
        return False
