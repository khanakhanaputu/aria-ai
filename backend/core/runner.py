import subprocess
import os
import re
import aiosqlite
from datetime import datetime
from pathlib import Path

# Sandbox paths
ALLOWED_PATHS = [
    Path(os.path.expanduser("~/Desktop")),
    Path(os.path.expanduser("~/Documents")),
]

# Whitelist command prefixes
ALLOWED_COMMANDS = [
    # File & folder management
    "mkdir",
    "md",
    "copy",
    "xcopy",
    "move",
    "del",
    "rmdir",
    "rd",
    "rename",
    "ren",
    "type",
    "echo",
    "dir",
    # App launcher
    "start",
    "explorer",
    # Process
    "taskkill",
    # Info
    "whoami",
    "hostname",
    "date",
    "time",
    "ver",
]

# Blocked keywords — selalu ditolak meski ada di whitelist
BLOCKED_KEYWORDS = [
    "reg ",
    "regedit",
    "netsh",
    "bcdedit",
    "format",
    "shutdown",
    "restart",
    "curl",
    "wget",
    "ssh",
    "powershell -enc",
    "invoke-expression",
    "iex",
    "rm -rf",
    "del /f /s /q c:\\",
]

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/memory.db")


async def init_runner_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS command_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT,
                output TEXT,
                status TEXT,
                executed_at TEXT
            )
        """
        )
        await db.commit()


async def log_command(command: str, output: str, status: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO command_log (command, output, status, executed_at) VALUES (?, ?, ?, ?)",
            (command, output, status, datetime.now().isoformat()),
        )
        await db.commit()


async def get_command_logs(limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM command_log ORDER BY executed_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


def is_path_safe(command: str) -> bool:
    """Cek apakah path dalam command ada di dalam sandbox."""
    # Extract semua path-like string dari command
    path_pattern = re.compile(r'[A-Za-z]:\\[^\s"\']+|"[A-Za-z]:\\[^"]+"')
    found_paths = path_pattern.findall(command)

    if not found_paths:
        return True  # Tidak ada absolute path, aman

    for p in found_paths:
        p_clean = p.strip('"')
        path_obj = Path(p_clean)
        if not any(
            str(path_obj).lower().startswith(str(allowed).lower())
            for allowed in ALLOWED_PATHS
        ):
            return False
    return True


def validate_command(command: str) -> tuple[bool, str]:
    """
    Return (is_safe, reason)
    """
    cmd_lower = command.strip().lower()

    # Cek blocked keywords dulu
    for blocked in BLOCKED_KEYWORDS:
        if blocked.lower() in cmd_lower:
            return False, f"Command mengandung keyword yang diblokir: `{blocked}`"

    # Cek whitelist
    first_word = cmd_lower.split()[0] if cmd_lower else ""
    if first_word not in [c.lower() for c in ALLOWED_COMMANDS]:
        return False, f"Command `{first_word}` tidak ada di whitelist"

    # Cek path sandbox
    if not is_path_safe(command):
        allowed_str = ", ".join(str(p) for p in ALLOWED_PATHS)
        return False, f"Path di luar sandbox. Hanya diizinkan di: {allowed_str}"

    return True, "ok"


async def execute_command(command: str) -> dict:
    """Eksekusi command dan return hasilnya."""
    is_safe, reason = validate_command(command)

    if not is_safe:
        await log_command(command, reason, "blocked")
        return {
            "status": "blocked",
            "command": command,
            "output": reason,
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(ALLOWED_PATHS[0]),  # Default CWD = Desktop
        )
        output = result.stdout or result.stderr or "(no output)"
        status = "success" if result.returncode == 0 else "error"
        await log_command(command, output, status)
        return {
            "status": status,
            "command": command,
            "output": output,
            "return_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        await log_command(command, "Timeout after 15s", "timeout")
        return {
            "status": "timeout",
            "command": command,
            "output": "Command timeout setelah 15 detik",
        }
    except Exception as e:
        await log_command(command, str(e), "error")
        return {
            "status": "error",
            "command": command,
            "output": str(e),
        }
