# 🔬 Research Assistant

A **Retrieval-Augmented Generation (RAG)** application that lets you upload PDF documents and ask natural language questions about them. It uses OpenAI embeddings stored in a PostgreSQL vector database (via `pgvector`) to retrieve the most relevant context and generate accurate answers with GPT-4o-mini.

---

## ✨ Features

- 📄 **PDF Ingestion** — Load and chunk PDF documents automatically
- 🧠 **Vector Embeddings** — Generate OpenAI embeddings (`text-embedding-ada-002`) for each chunk
- 🗄️ **PostgreSQL + pgvector** — Persist and query embeddings using cosine similarity search
- 💬 **Q&A Interface** — Interactive CLI to ask questions and get context-grounded answers
- ⚡ **LangChain Powered** — Built on LangChain for document loading, splitting, and LLM interaction

---

## 🏗️ Architecture

```
PDF File
   │
   ▼
loader.py  ──► load_document()      # PyPDFLoader
               chunk_documents()    # RecursiveCharacterTextSplitter (300 chars, 30 overlap)
   │
   ▼
rag.py     ──► create_embedding()   # OpenAIEmbeddings → vectors
   │
   ▼
database.py──► store_in_database()  # SQLAlchemy + pgvector (Documents table)
   │
   ▼
         [ PostgreSQL + pgvector ]
   │
   ▼
database.py──► retrieve_content()   # cosine_distance query, top-5 chunks
   │
   ▼
rag.py     ──► generate_answer()    # GPT-4o-mini with context prompt
   │
   ▼
         Answer printed to console
```

---

## 📁 Project Structure

```
research_assistant/
├── app/
│   ├── main.py         # Entry point: ingests document and runs Q&A loop
│   ├── loader.py       # PDF loading and text chunking
│   ├── rag.py          # Embedding creation and answer generation (OpenAI)
│   └── database.py     # SQLAlchemy models, vector storage, and retrieval
├── uploads/            # Place your PDF files here
├── migrations/         # Alembic database migration files
├── alembic.ini         # Alembic configuration
├── docker-compose.yml  # (Optional) Docker setup for PostgreSQL
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL with the [`pgvector`](https://github.com/pgvector/pgvector) extension enabled
- An [OpenAI API key](https://platform.openai.com/api-keys)

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
DATABASE_URL=postgresql://user:password@localhost:5432/research_assistant
```

### 5. Set Up the Database

Make sure PostgreSQL is running and the `pgvector` extension is installed:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The application will automatically create the `documents` table on first run.

### 6. Add Your PDF

Place your PDF in the `uploads/` folder and update the file path in [`app/main.py`](app/main.py):

```python
file_path = "uploads/your-document.pdf"
file_name = "your-document.pdf"
```

### 7. Run the Application

```bash
cd app
python main.py
```

The script will:
1. **Ingest** the PDF — load, chunk, embed, and store it in the database
2. **Start a Q&A loop** — type any question and receive a grounded answer

---

## 🛠️ Tech Stack

| Component         | Technology                        |
|-------------------|-----------------------------------|
| Language          | Python 3.10+                      |
| LLM               | OpenAI GPT-4o-mini                |
| Embeddings        | OpenAI `text-embedding-ada-002`   |
| Vector DB         | PostgreSQL + pgvector             |
| ORM               | SQLAlchemy 2.0                    |
| Document Loading  | LangChain / PyPDFLoader           |
| Text Splitting    | RecursiveCharacterTextSplitter    |
| Migrations        | Alembic                           |
| API Framework     | FastAPI / Uvicorn (available)     |

---

## ⚙️ Configuration

| Parameter      | Location         | Default         | Description                          |
|----------------|------------------|-----------------|--------------------------------------|
| `chunk_size`   | `loader.py`      | `300`           | Characters per chunk                 |
| `chunk_overlap`| `loader.py`      | `30`            | Overlap between consecutive chunks   |
| `top_k`        | `database.py`    | `5`             | Number of chunks retrieved per query |
| `model`        | `rag.py`         | `gpt-4o-mini`   | OpenAI chat model used for answers   |

---

## 📦 Key Dependencies

- [`langchain`](https://github.com/langchain-ai/langchain) — Document loading, splitting, and LLM orchestration
- [`langchain-openai`](https://pypi.org/project/langchain-openai/) — OpenAI embeddings and chat models
- [`pgvector`](https://github.com/pgvector/pgvector-python) — Vector similarity search in PostgreSQL
- [`SQLAlchemy`](https://www.sqlalchemy.org/) — Database ORM
- [`pypdf`](https://pypdf.readthedocs.io/) — PDF parsing
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — Environment variable management
- [`alembic`](https://alembic.sqlalchemy.org/) — Database migrations
- [`fastapi`](https://fastapi.tiangolo.com/) / [`uvicorn`](https://www.uvicorn.org/) — API server (available for extension)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
