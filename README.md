# 🔬 Research Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![LangGraph](https://img.shields.io/badge/LangGraph-latest-FF6B35?style=flat)](https://github.com/langchain-ai/langgraph)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A full-stack **Retrieval-Augmented Generation (RAG)** research assistant — upload PDF documents, ask natural language questions about them, and get streaming answers with source citations. Falls back to live web search when documents don't cover the topic.

Built with **FastAPI**, **LangGraph**, **OpenAI**, **PostgreSQL + pgvector**, and a **React + Vite** frontend.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 📄 **PDF Ingestion** | Upload PDFs via the UI or REST API; chunking and embedding run in the background |
| 🧠 **Semantic Search** | OpenAI embeddings stored in PostgreSQL with `pgvector`; similarity-score threshold filters irrelevant chunks |
| 🤖 **LangGraph Agent** | Multi-step agentic pipeline: retrieve → grade → generate or web-search |
| 🌐 **Web Search Fallback** | DuckDuckGo search kicks in automatically when uploaded documents don't contain the answer |
| 📚 **Source Citations** | PDF citations (filename + page number + preview) rendered below AI answers |
| 💬 **Conversation Memory** | Per-session chat history persisted in PostgreSQL; survives page refreshes |
| ⚡ **Token Streaming** | Word-by-word streamed responses via `ReadableStream` — no waiting for the full answer |
| 📝 **Document Summarization** | One-click map-reduce summarization for any uploaded PDF |
| 🎨 **ChatGPT-style UI** | Dark theme (`#212121`), file attachment chips, markdown rendering, source cards |
| 🐳 **Docker Ready** | Single command to spin up the full PostgreSQL + pgvector stack |

---

## 🏗️ Architecture

### LangGraph Agent Flow

```
User Question
     │
     ▼
load_history_node    ← load conversation history from PostgreSQL
     │
     ▼
retrieve_node        ← similarity search with score threshold (≥ 0.65)
     │
     ▼
grade_retrieval_node ← Stage 1: empty context? → web. Stage 2: LLM grades sufficiency
     │
     ├─── relevant ────────────────────────────────┐
     │                                             │
     └─── not relevant ──► web_search_node         │
                           (DuckDuckGo)            │
                                │                  │
                                └────── generate_node ◄┘
                                             │
                                    save_messages_node ← persist Q&A to PostgreSQL
                                             │
                                           Answer + Sources
```

**Key design decisions:**
- Streaming filters by `langgraph_node == "generate"` — grading tokens never reach the UI
- Sources are captured from the `generate` node's state update during streaming (no post-hoc `get_state()`)
- When the web-search path is taken, `generate_node` explicitly returns `sources: []` to clear PDF citations
- Conversation history is capped at the last 10 messages to stay within token limits

---

### Project Structure

```
research_assistant/
├── app/
│   ├── core/
│   │   ├── config.py           # Pydantic Settings — single source of env vars
│   │   └── database.py         # SQLAlchemy models + session helpers (indexed on session_id)
│   ├── rag/
│   │   ├── loader.py           # PDF loading + text chunking
│   │   ├── store.py            # PGVector store + similarity-score-threshold retriever
│   │   └── generator.py        # Map-reduce document summarization
│   ├── graph/
│   │   ├── state.py            # GraphState TypedDict (shared agent state)
│   │   ├── nodes.py            # All LangGraph node functions
│   │   ├── edges.py            # Conditional routing logic
│   │   ├── checkpoint.py       # PostgreSQL-backed LangGraph checkpointer
│   │   └── builder.py          # Graph assembly — exports compiled `graph`
│   └── api/
│       ├── routes.py           # FastAPI endpoint handlers
│       └── streaming.py        # Token streaming with dual stream_mode
├── frontend/                   # React + Vite frontend
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js       # Fetch wrappers for all API endpoints
│   │   ├── components/
│   │   │   ├── ChatArea.jsx    # Message list + input bar container
│   │   │   ├── InputBar.jsx    # Textarea with file attachment chip
│   │   │   ├── MessageBubble.jsx  # User/AI/upload message rendering + markdown
│   │   │   ├── Sidebar.jsx     # Document list + upload button
│   │   │   ├── SummaryModal.jsx   # Document summary popup
│   │   │   └── Toast.jsx       # Notification toasts
│   │   ├── hooks/
│   │   │   ├── useChat.js      # Streaming chat state + upload message helpers
│   │   │   ├── useDocuments.js # Document list, upload, delete
│   │   │   └── useSession.js   # UUID session persistence via localStorage
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css           # ChatGPT-style design tokens + all component styles
│   ├── package.json
│   └── vite.config.js
├── migrations/                 # Alembic migration files
├── main.py                     # CLI entry point for local testing
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
└── .env                        # Local secrets (not committed)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for the frontend)
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

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/research_assistant
```

### 5. Start the Database

```bash
docker-compose up -d
```

> Starts a PostgreSQL 16 container with the `pgvector` extension pre-installed.

### 6. Run Database Migrations

```bash
alembic upgrade head
```

### 7. Start the Backend API

```bash
uvicorn app.api.routes:app --reload
```

API available at **http://localhost:8000** · Swagger UI at **http://localhost:8000/docs**

### 8. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at **http://localhost:5173**

---

## 🖥️ Using the UI

1. **Upload a PDF** — click the upload button in the left sidebar. A file card appears in the chat and an attachment chip appears in the input bar.
2. **Ask a question** — type in the input box and press **Enter**. The answer streams in word-by-word.
3. **View sources** — if the answer came from your documents, source cards (filename + page number + preview) appear below the response.
4. **Web fallback** — if your documents don't cover the topic, the assistant automatically searches the web. No source cards are shown in this case.
5. **Summarize a document** — hover a document in the sidebar and click the 📝 icon.
6. **New chat** — click "New Chat" in the sidebar to start a fresh session.

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a PDF — chunking and embedding run in the background |
| `POST` | `/ask` | Ask a question — returns a single JSON response |
| `POST` | `/ask_stream` | Ask a question — streams tokens as plain text |
| `GET` | `/documents` | List all uploaded document names |
| `DELETE` | `/documents/{file_name}` | Delete all chunks for a document |
| `POST` | `/summarize` | Summarize an uploaded document |

### Example: Upload a PDF

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@your-document.pdf"
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

For quick local testing without the full stack:

```bash
# 1. Place your PDF in the uploads/ directory
# 2. Update FILE_PATH in main.py
# 3. Run:
python main.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend Language** | Python 3.10+ |
| **API Framework** | FastAPI + Uvicorn |
| **Agent Orchestration** | LangGraph |
| **LLM** | OpenAI GPT-4o-mini |
| **Embeddings** | OpenAI `text-embedding-ada-002` |
| **Vector Store** | PostgreSQL + pgvector |
| **ORM** | SQLAlchemy 2.0 |
| **Settings** | Pydantic Settings |
| **Document Loading** | LangChain / PyPDFLoader |
| **Web Search Fallback** | DuckDuckGo Search |
| **Migrations** | Alembic |
| **Containerization** | Docker + docker-compose |
| **Frontend Framework** | React 18 + Vite |
| **Markdown Rendering** | react-markdown |
| **Styling** | Vanilla CSS (ChatGPT-style dark theme) |

---

## ⚙️ Configuration

Key parameters you can tune directly in the source:

| Parameter | File | Default | Description |
|-----------|------|---------|-------------|
| `chunk_size` | `app/rag/loader.py` | `1000` | Characters per document chunk |
| `chunk_overlap` | `app/rag/loader.py` | `100` | Overlap between consecutive chunks |
| `score_threshold` | `app/rag/store.py` | `0.65` | Min cosine similarity for retrieval (raise = stricter, lower = more permissive) |
| `k` | `app/rag/store.py` | `5` | Max chunks returned per query |
| `model` | `app/graph/nodes.py` | `gpt-4o-mini` | OpenAI chat model |
| `history_limit` | `app/graph/nodes.py` | `10` | Max recent messages sent to LLM |

---

## 🔧 Troubleshooting

**`pgvector` extension not found**
Make sure you're using the Docker container from this repo (`docker-compose up -d`), which bundles pgvector. If using an external PostgreSQL instance, run `CREATE EXTENSION IF NOT EXISTS vector;` manually.

**Alembic migration fails with `relation already exists`**
Run `alembic stamp head` to mark the current state, then retry.

**`OPENAI_API_KEY` not found**
Ensure your `.env` file is in the project root and that you've activated your virtual environment. Check for trailing spaces around the `=` sign.

**Streaming response cuts off early**
Some reverse proxies (nginx, Caddy) buffer responses by default. Add `X-Accel-Buffering: no` to your proxy config or connect directly to uvicorn during development.

**PDF upload returns 500**
The `uploads/` directory must exist. Create it with `mkdir uploads` if missing.

**Answer says "context does not contain" for a document question**
The similarity threshold (`score_threshold = 0.65`) may be too high for your document type. Lower it to `0.5` in `app/rag/store.py`.

**Web search triggering for document questions**
The grading LLM may be returning "no" too aggressively. Check that your question is specific enough to match document content, or lower `score_threshold` slightly.

**Frontend can't reach the API**
Ensure the backend is running on port 8000 and the Vite proxy in `vite.config.js` points to `http://localhost:8000`.

---

## 📦 Key Dependencies

- [`langchain`](https://github.com/langchain-ai/langchain) — Document loading and text splitting
- [`langgraph`](https://github.com/langchain-ai/langgraph) — Stateful multi-step agent framework
- [`langchain-openai`](https://pypi.org/project/langchain-openai/) — OpenAI embeddings and chat models
- [`langchain-postgres`](https://pypi.org/project/langchain-postgres/) — PGVector integration
- [`fastapi`](https://fastapi.tiangolo.com/) / [`uvicorn`](https://www.uvicorn.org/) — ASGI web framework and server
- [`SQLAlchemy`](https://www.sqlalchemy.org/) — Database ORM
- [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — Type-safe env variable management
- [`alembic`](https://alembic.sqlalchemy.org/) — Database schema migrations
- [`react-markdown`](https://github.com/remarkjs/react-markdown) — Markdown rendering in the frontend

---

## 📄 License

This project is open source and for educational purposes.
