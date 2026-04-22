from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.chat import router as chat_router
from backend.routers.system import router as system_router
from backend.routers.runner import router as runner_router
from backend.routers.files import router as files_router
from backend.core.memory import init_db
from backend.core.runner import init_runner_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Aria AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(system_router)
app.include_router(runner_router)
app.include_router(files_router)


@app.on_event("startup")
async def startup():
    await init_db()
    await init_runner_db()


@app.get("/")
async def root():
    return {"message": "Aria AI Backend is running"}
