# 🔬 Research Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-FF6B35?style=flat)](https://github.com/langchain-ai/langgraph)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-ready **Retrieval-Augmented Generation (RAG)** API — upload PDF documents and ask natural language questions about them, with streaming responses, conversation memory, and automatic web search fallback.

Built with **FastAPI**, **LangGraph**, **OpenAI**, and **PostgreSQL + pgvector**.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 📄 **PDF Ingestion** | Upload PDFs via REST API; chunking and embedding run in the background |
| 🧠 **Vector Search** | OpenAI embeddings stored in PostgreSQL with `pgvector` for cosine similarity retrieval |
| 🤖 **LangGraph Agent** | Multi-step agentic pipeline with retrieval grading and automatic web search fallback |
| 💬 **Conversation Memory** | Per-session chat history persisted in PostgreSQL |
| ⚡ **Streaming** | Token-by-token streamed responses via Server-Sent Events (SSE) |
| 📝 **Summarization** | One-call summarization of any uploaded document |
| 🐳 **Docker Ready** | Single command to spin up the full PostgreSQL + pgvector stack |

---

## 🏗️ Architecture

### LangGraph Agent Flow

```
User Question
     │
     ▼
load_history_node   ← load conversation history from PostgreSQL
     │
     ▼
retrieve_node       ← cosine similarity search (top-5 chunks)
     │
     ▼
grade_retrieval_node ← LLM grades: is the retrieved context sufficient?
     │
     ├─── YES ─────────────────────────────────┐
     │                                         │
     └─── NO ──► web_search_node               │
                 (DuckDuckGo fallback)          │
                      │                        │
                      └──────── generate_node ◄┘
                                     │
                                     ▼
                             save_messages_node ← persist Q&A to PostgreSQL
                                     │
                                     ▼
                                  Answer
```

### Project Structure

```
research_assistant/
├── main.py                     # CLI entry point for local testing
├── app/
│   ├── core/
│   │   ├── config.py           # Pydantic Settings — single source of env vars
│   │   └── database.py         # SQLAlchemy models + all DB session helpers
│   ├── rag/
│   │   ├── loader.py           # PDF loading + text chunking
│   │   ├── store.py            # PGVector store creation + retriever factory
│   │   └── generator.py        # LLM answer generation + summarization
│   ├── graph/
│   │   ├── state.py            # GraphState TypedDict (shared agent state)
│   │   ├── nodes.py            # All LangGraph node functions
│   │   ├── edges.py            # Conditional routing logic
│   │   ├── checkpoint.py       # PostgreSQL-backed LangGraph memory
│   │   └── builder.py          # Graph assembly — exports compiled `graph`
│   └── api/
│       ├── routes.py           # All FastAPI endpoint handlers
│       └── streaming.py        # SSE token streaming generator
├── uploads/                    # Place PDFs here (for CLI mode)
├── migrations/                 # Alembic migration files
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── .env                        # Local secrets (not committed to git)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Docker** (for PostgreSQL + pgvector)
- An **[OpenAI API key](https://platform.openai.com/api-keys)**

---

### 1. Clone the Repository

```bash
git clone https://github.com/DevSaadSaboor/research_assistant.git
cd research_assistant
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/research_assistant
```

### 5. Start the Database

```bash
docker-compose up -d
```

> This starts a PostgreSQL 16 container with the `pgvector` extension pre-installed. No manual `CREATE EXTENSION` step is required.

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the API Server

```bash
uvicorn app.api.routes:app --reload
```

The API will be available at **http://localhost:8000**.  
Open **http://localhost:8000/docs** for the interactive Swagger UI.

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a PDF — embedding runs in the background |
| `POST` | `/ask` | Ask a question — returns a single JSON response |
| `POST` | `/ask_stream` | Ask a question — streams tokens via SSE |
| `GET` | `/documents` | List all uploaded document names |
| `DELETE` | `/documents/{file_name}` | Delete all chunks for a document |
| `POST` | `/summarize` | Summarize an uploaded document |

### Example: Upload a PDF

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@your-document.pdf"
```

### Example: Ask a Question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"session_id": "my-session", "question": "What is the main topic?"}'
```

### Example: Streaming Response

```bash
curl -X POST http://localhost:8000/ask_stream \
  -H "Content-Type: application/json" \
  -d '{"session_id": "my-session", "question": "Summarize the key findings."}'
```

### Example: Summarize a Document

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"file_name": "your-document.pdf"}'
```

---

## 💻 CLI Mode

For quick local testing without running the full API server:

```bash
# 1. Place your PDF in the uploads/ directory
# 2. Update FILE_PATH in main.py to point to your PDF
# 3. Run:
python main.py
```

CLI mode runs the full LangGraph pipeline locally — same retrieval, grading, and generation logic as the API, without needing `uvicorn` or any HTTP client.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| API Framework | FastAPI + Uvicorn |
| Agent Orchestration | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI `text-embedding-ada-002` |
| Vector Store | PostgreSQL + pgvector |
| ORM | SQLAlchemy 2.0 |
| Settings | Pydantic Settings |
| Document Loading | LangChain / PyPDFLoader |
| Web Search Fallback | DuckDuckGo Search |
| Migrations | Alembic |
| Containerization | Docker + docker-compose |

---

## ⚙️ Configuration

The following parameters can be tuned directly in the source:

| Parameter | File | Default | Description |
|-----------|------|---------|-------------|
| `chunk_size` | `app/rag/loader.py` | `1000` | Characters per document chunk |
| `chunk_overlap` | `app/rag/loader.py` | `100` | Overlap between consecutive chunks |
| `top_k` | `app/rag/store.py` | `5` | Number of chunks retrieved per query |
| `model` | `app/rag/generator.py` | `gpt-4o-mini` | OpenAI chat model used for generation |

---

## 🔧 Troubleshooting

**`pgvector` extension not found**  
Make sure you're using the Docker container from this repo (`docker-compose up -d`), which bundles pgvector. If using an external PostgreSQL instance, run `CREATE EXTENSION IF NOT EXISTS vector;` manually.

**Alembic migration fails with `relation already exists`**  
Your database may already be partially initialized. Run `alembic stamp head` to mark the current state, then retry.

**`OPENAI_API_KEY` not found**  
Ensure your `.env` file is in the project root and that you've activated your virtual environment before starting the server. Double-check there are no trailing spaces around the `=` sign.

**Streaming response cuts off early**  
Some reverse proxies (nginx, Caddy) buffer SSE by default. Add `X-Accel-Buffering: no` to your proxy config or connect directly to uvicorn during development.

**PDF upload returns 500**  
The `uploads/` directory must exist and be writable. Create it with `mkdir -p uploads` if it's missing.

**Web search fallback not triggering**  
The grading step uses the LLM to decide if retrieved context is sufficient. If your document covers the topic, the fallback won't activate — this is expected behavior.

---

## 📦 Key Dependencies

- [`langchain`](https://github.com/langchain-ai/langchain) — Document loading and text splitting
- [`langgraph`](https://github.com/langchain-ai/langgraph) — Stateful multi-step agent framework
- [`langchain-openai`](https://pypi.org/project/langchain-openai/) — OpenAI embeddings and chat models
- [`langchain-postgres`](https://pypi.org/project/langchain-postgres/) — PGVector integration
- [`pgvector`](https://github.com/pgvector/pgvector-python) — Vector similarity search in PostgreSQL
- [`SQLAlchemy`](https://www.sqlalchemy.org/) — Database ORM
- [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — Type-safe environment variable management
- [`fastapi`](https://fastapi.tiangolo.com/) / [`uvicorn`](https://www.uvicorn.org/) — ASGI web framework and server
- [`alembic`](https://alembic.sqlalchemy.org/) — Database schema migrations

---

## 📄 License

This project is open source and for educational purpose
