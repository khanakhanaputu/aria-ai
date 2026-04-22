from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.core.ollama import chat, chat_stream, is_ollama_running
from backend.core.memory import (
    create_session,
    get_sessions,
    get_messages,
    save_message,
    delete_session,
    update_session_title,
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: int | None = None


class SessionCreate(BaseModel):
    title: str = "New Chat"


class SessionRename(BaseModel):
    title: str


@router.get("/health")
async def health():
    ollama_ok = await is_ollama_running()
    if not ollama_ok:
        raise HTTPException(status_code=503, detail="Ollama is not running")
    return {"status": "ok", "ollama": True}


@router.get("/sessions")
async def list_sessions():
    return await get_sessions()


@router.post("/sessions")
async def new_session(body: SessionCreate):
    session_id = await create_session(body.title)
    return {"session_id": session_id}


@router.get("/sessions/{session_id}/messages")
async def list_messages(session_id: int):
    return await get_messages(session_id)


@router.delete("/sessions/{session_id}")
async def remove_session(session_id: int):
    await delete_session(session_id)
    return {"status": "deleted"}


@router.patch("/sessions/{session_id}")
async def rename_session(session_id: int, body: SessionRename):
    await update_session_title(session_id, body.title)
    return {"status": "updated"}


@router.post("/stream")
async def stream_message(req: ChatRequest):
    from backend.core.ollama import generate_title

    session_id = req.session_id
    is_new_session = not session_id

    if not session_id:
        session_id = await create_session()

    history = await get_messages(session_id)

    await save_message(session_id, "user", req.message)

    # Trim — ambil 20 pesan terakhir saja
    MAX_HISTORY = 20
    trimmed_history = history[-MAX_HISTORY:] if len(history) > MAX_HISTORY else history
    messages = trimmed_history + [{"role": "user", "content": req.message}]

    full_reply = []

    async def generator():
        async for token in chat_stream(messages):
            full_reply.append(token)
            yield token

        reply_text = "".join(full_reply)
        await save_message(session_id, "assistant", reply_text)

        if is_new_session:
            title = await generate_title(req.message)
            await update_session_title(session_id, title)

        yield f"\n\n[SESSION_ID:{session_id}]"

    return StreamingResponse(
        generator(), media_type="text/plain", headers={"X-Session-Id": str(session_id)}
    )
