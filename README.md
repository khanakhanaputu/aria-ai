# 🤖 Aria AI

A fully local AI assistant with a modern web UI and CLI, powered by [Ollama](https://ollama.com). Aria runs entirely on your machine — no cloud, no API keys, no data leaving your computer.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)
![Vue](https://img.shields.io/badge/Vue-3-brightgreen?style=flat-square&logo=vue.js)
![Ollama](https://img.shields.io/badge/Ollama-local-orange?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-purple?style=flat-square)

---

## ✨ Features

### 💬 Chat Interface
- Streaming responses (token by token, like ChatGPT)
- Full markdown rendering with syntax-highlighted code blocks
- Persistent chat history with auto-generated session titles
- Session management — create, rename, delete conversations

### 📊 System Monitor
- Live CPU, RAM, and GPU usage (auto-refresh every 3s)
- GPU temperature and VRAM tracking via NVML
- Top process list sorted by memory usage
- Toggleable side panel inside the chat UI

### ⚡ Command Runner
- Natural language to shell command via AI
- Security whitelist — only safe commands are allowed
- Preview & confirm before execution
- Full audit log of all executed commands

### ⚙️ Settings
- Switch between installed Ollama models
- System status overview
- Clear all chat history

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Engine | Ollama (`qwen2.5:3b` recommended) |
| Backend | Python + FastAPI |
| Memory | SQLite via aiosqlite |
| GPU Monitoring | pynvml |
| Frontend | Vue 3 + shadcn-vue + Tailwind CSS |
| State Management | Pinia |

---

## 📋 Requirements

- Windows 10/11
- Python 3.11+
- Node.js 18+
- [Ollama](https://ollama.com) installed and running
- NVIDIA GPU with drivers (optional, but recommended)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/aria-ai.git
cd aria-ai
```

### 2. Pull an Ollama model

```bash
ollama pull qwen2.5:3b
```

### 3. Set up the backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and adjust if needed:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:3b
APP_HOST=127.0.0.1
APP_PORT=8000
```

### 5. Start the backend

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Set up and start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 7. Open the app

Visit `http://localhost:5173` in your browser.

---

## 📁 Project Structure

```
aria-ai/
├── backend/
│   ├── core/
│   │   ├── ollama.py       # Ollama communication + streaming
│   │   ├── memory.py       # SQLite session & message storage
│   │   ├── system.py       # CPU/RAM/GPU monitoring
│   │   └── runner.py       # Shell command execution & validation
│   ├── routers/
│   │   ├── chat.py         # Chat & session endpoints
│   │   ├── system.py       # System monitor endpoints
│   │   └── runner.py       # Command runner endpoints
│   └── main.py             # FastAPI app entry point
├── frontend/
│   └── src/
│       ├── components/     # Vue components (Chat, System, Runner)
│       ├── views/          # Page views (Chat, Settings)
│       ├── stores/         # Pinia state management
│       └── services/       # API service layer
├── data/
│   └── memory.db           # SQLite database (auto-created)
├── .env                    # Environment config (not committed)
└── requirements.txt
```

---

## 🔒 Command Runner Security

The command runner uses a strict whitelist approach:

- **Allowed commands:** `mkdir`, `copy`, `move`, `del`, `rename`, `start`, `explorer`, `taskkill`, `dir`, `echo`, `type`, `whoami`
- **Blocked keywords:** registry access, network tools, system config commands
- **Sandbox paths:** Commands involving file paths are restricted to `Desktop` and `Documents` by default
- **Audit log:** Every executed command is logged to SQLite with its output and status

---

## 🗺️ Roadmap

- [x] Streaming chat with Ollama
- [x] Persistent session memory
- [x] System monitor dashboard
- [x] Shell command runner with security whitelist
- [x] Settings page with model switcher
- [ ] Background daemon for proactive interventions
- [ ] Terminal UI (Textual/Rich)
- [ ] Personal knowledge base & snippet manager
- [ ] Active window/process context awareness

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

> Built with ❤️ using Ollama, FastAPI, and Vue 3.
