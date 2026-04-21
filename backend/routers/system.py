from fastapi import APIRouter
from backend.core.system import (
    get_full_status,
    get_cpu,
    get_ram,
    get_gpu,
    get_processes,
)
import httpx
import os

router = APIRouter(prefix="/system", tags=["system"])

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


@router.get("/")
async def full_status():
    return get_full_status()


@router.get("/cpu")
async def cpu():
    return get_cpu()


@router.get("/ram")
async def ram():
    return get_ram()


@router.get("/gpu")
async def gpu():
    return get_gpu()


@router.get("/processes")
async def processes(limit: int = 10):
    return get_processes(limit)


@router.get("/models")
async def get_models():
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("models", [])]
