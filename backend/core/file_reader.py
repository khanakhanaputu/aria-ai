import os
from pathlib import Path

# Max ukuran file yang dibaca (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

SUPPORTED_TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".vue",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".scss",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".env",
    ".ini",
    ".cfg",
    ".toml",
    ".sh",
    ".bat",
    ".ps1",
    ".sql",
    ".xml",
    ".csv",
    ".c",
    ".cpp",
    ".h",
    ".java",
    ".go",
    ".rs",
    ".php",
    ".rb",
}


def read_text_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def read_pdf_file(filepath: str) -> str:
    import fitz  # pymupdf

    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_file_content(filepath: str, filename: str) -> dict:
    ext = Path(filename).suffix.lower()
    size = os.path.getsize(filepath)

    if size > MAX_FILE_SIZE:
        return {
            "success": False,
            "error": f"File too large ({round(size/1e6, 1)}MB). Max is 5MB.",
            "filename": filename,
        }

    try:
        if ext == ".pdf":
            content = read_pdf_file(filepath)
            file_type = "PDF"
        elif ext in SUPPORTED_TEXT_EXTENSIONS:
            content = read_text_file(filepath)
            file_type = "text"
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {ext}",
                "filename": filename,
            }

        # Trim kalau terlalu panjang (max ~8000 karakter)
        MAX_CHARS = 8000
        trimmed = False
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            trimmed = True

        return {
            "success": True,
            "filename": filename,
            "file_type": file_type,
            "content": content,
            "trimmed": trimmed,
            "size_kb": round(size / 1024, 1),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filename": filename,
        }
