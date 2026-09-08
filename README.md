# CNC Cutting Tool Intelligent Q&A System

An intelligent CNC cutting tool Q&A system powered by multiple agents and retrieval-augmented generation (RAG). It supports tool selection, parameter recommendations, model interpretation, machining fault diagnosis, streaming Q&A, knowledge retrieval, conversation history, sales order inquiries, and nearby supplier searches.

Project identifier: `tools-multi-agent`

## Key Features

- CNC cutting tool selection, model, and compatibility consultation
- Cutting parameter calculation and machining fault diagnosis
- Markdown document upload and RAG retrieval
- Multi-agent task recognition and automatic routing
- SSE streaming responses with tool-call progress
- Conversation history storage and recovery
- Sales order inquiries and nearby supplier searches

## Tech Stack

- Frontend: Vue 3, Vite, Element Plus
- Backend: Python, FastAPI, OpenAI Agents SDK
- Knowledge base: LangChain, Chroma, Jieba, and embedding models
- External services: OpenAI-compatible model APIs and Baidu Maps MCP

## Project Structure

```text
backend/
  app/                    # Multi-agent backend
  knowledge_new/          # RAG knowledge base backend
front/
  agent_web_ui/           # Main chat frontend
  knowledge_platform_ui/  # Knowledge management frontend
README.md                 # Chinese documentation
README_EN.md              # English documentation
```

## Requirements

- Python 3.11
- Node.js 18+
- npm 9+
- Conda (recommended) or Python venv

## Installation

Use separate Python environments for the two backend services.

### Knowledge Base Backend

```bash
cd backend/knowledge_new
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Multi-Agent Backend

```bash
cd backend/app
python -m pip install -r requirements.txt
python -m pip install -e .
```

### Frontends

```bash
cd front/agent_web_ui
npm install

cd ../knowledge_platform_ui
npm install
```

## Environment Variables

Copy the environment variable templates:

```powershell
Copy-Item backend/knowledge_new/.env.example backend/knowledge_new/.env
Copy-Item backend/app/.env.example backend/app/.env
```

Fill in the required model, embedding, and map service settings. Never commit `.env` files containing real credentials.

## Quick Start

Start each service in a separate terminal in the following order.

### 1. Knowledge Base Backend

```bash
cd backend/knowledge_new
python -m api.main
```

- API: `http://127.0.0.1:8001`
- API documentation: `http://127.0.0.1:8001/docs`

### 2. Multi-Agent Backend

```bash
cd backend/app
python -m api.main
```

- API: `http://127.0.0.1:8000`
- API documentation: `http://127.0.0.1:8000/docs`

### 3. Main Chat Frontend

```bash
cd front/agent_web_ui
npm run dev
```

Open `http://localhost:5173`.

### 4. Knowledge Management Frontend (Optional)

```bash
cd front/knowledge_platform_ui
npm run dev
```

Open `http://localhost:3000`.

## Initialize the Knowledge Base

```bash
cd backend/knowledge_new
python -m cli.upload_cli
```

Knowledge documents are stored in `backend/knowledge_new/data/cutting_tool/` by default.
