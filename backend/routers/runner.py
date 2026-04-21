from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.runner import execute_command, validate_command, get_command_logs
from backend.core.ollama import chat

router = APIRouter(prefix="/runner", tags=["runner"])


class NaturalCommandRequest(BaseModel):
    instruction: str


class DirectCommandRequest(BaseModel):
    command: str


class ValidateRequest(BaseModel):
    command: str


@router.post("/parse")
async def parse_instruction(req: NaturalCommandRequest):
    """Konversi natural language ke shell command, tapi belum eksekusi."""
    prompt = f"""You are a Windows CMD assistant. Convert the user's instruction into a single Windows CMD command.

Rules:
- Reply with ONLY the raw command, no explanation, no markdown, no backticks
- Use CMD syntax, not PowerShell
- Only use safe commands: mkdir, copy, move, del, rename, start, explorer, taskkill, dir, echo, type, whoami
- If the instruction is unsafe or impossible, reply with: UNSAFE: <reason>

Instruction: {req.instruction}
Command:"""

    messages = [{"role": "user", "content": prompt}]
    result = await chat(messages)
    command = result.strip()

    if command.upper().startswith("UNSAFE:"):
        return {
            "status": "unsafe",
            "instruction": req.instruction,
            "command": None,
            "reason": command[7:].strip(),
        }

    is_safe, reason = validate_command(command)

    return {
        "status": "ready" if is_safe else "blocked",
        "instruction": req.instruction,
        "command": command,
        "reason": reason if not is_safe else None,
    }


@router.post("/execute")
async def execute(req: DirectCommandRequest):
    """Eksekusi command langsung (setelah user konfirmasi)."""
    return await execute_command(req.command)


@router.post("/run")
async def run_natural(req: NaturalCommandRequest):
    """Parse + eksekusi langsung tanpa konfirmasi (untuk CLI mode)."""
    prompt = f"""You are a Windows CMD assistant. Convert the user's instruction into a single Windows CMD command.

Rules:
- Reply with ONLY the raw command, no explanation, no markdown, no backticks
- Use CMD syntax, not PowerShell
- Only use safe commands: mkdir, copy, move, del, rename, start, explorer, taskkill, dir, echo, type, whoami
- Command format: COMMAND [options] [path] — never put path before command
- For mkdir: always use `mkdir PATH` format, e.g. `mkdir E:\\ProjectAI` not `E:\\mkdir ProjectAI`
- If the instruction is unsafe or impossible, reply with: UNSAFE: <reason>

Examples:
- "create folder test on desktop" -> mkdir C:\\Users\\%USERNAME%\\Desktop\\test
- "create folder ProjectAI on E drive" -> mkdir E:\\ProjectAI
- "open documents folder" -> explorer C:\\Users\\%USERNAME%\\Documents

Instruction: {req.instruction}
Command:"""

    messages = [{"role": "user", "content": prompt}]
    result = await chat(messages)
    command = result.strip()

    if command.upper().startswith("UNSAFE:"):
        return {
            "status": "unsafe",
            "instruction": req.instruction,
            "command": None,
            "output": command[7:].strip(),
        }

    return await execute_command(command)


@router.get("/logs")
async def logs(limit: int = 20):
    return await get_command_logs(limit)


@router.post("/validate")
async def validate(req: ValidateRequest):
    is_safe, reason = validate_command(req.command)
    return {"safe": is_safe, "reason": reason}
