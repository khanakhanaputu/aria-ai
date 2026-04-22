from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.core.file_reader import extract_file_content
import tempfile
import os

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/read")
async def read_file(file: UploadFile = File(...)):
    # Simpan ke temp file dulu
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = extract_file_content(tmp_path, file.filename)
    finally:
        os.unlink(tmp_path)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
