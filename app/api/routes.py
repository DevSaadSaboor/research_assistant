import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.rag.loader import load_document, chunk_documents
from app.rag.store import create_vector_store, delete_from_vector_store
from app.rag.generator import summarize_document
from app.graph.builder import graph
from app.graph.checkpoint import setup_checkpointer, shutdown_checkpointer
from app.api.streaming import event_generator
from app.core.database import get_documents, delete_documents, get_document_content, init_db, store_document_chunks

@asynccontextmanager
async def lifespan(application: FastAPI):
    init_db()
    setup_checkpointer()
    yield
    shutdown_checkpointer()


app = FastAPI(
    title="Research Assistant API",
    description="Upload PDFs and ask questions powered by RAG + LangGraph.",
    version="1.0.0",
    lifespan=lifespan,
)


class QuestionRequest(BaseModel):
    session_id: str
    question: str

class SummaryRequest(BaseModel):
    file_name: str




def _process_documents(file_path: str) -> None:
    file_name = os.path.basename(file_path)
    documents = load_document(file_path)
    chunks = chunk_documents(documents)
    create_vector_store(chunks)       
    store_document_chunks(file_name, chunks)  


@app.post("/upload", summary="Upload a PDF and start background ingestion")
def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    safe_name = os.path.basename(file.filename)
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{safe_name}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    background_tasks.add_task(_process_documents, file_path)
    return {"message": "Document uploaded successfully. Processing started."}


@app.post("/ask", summary="Ask a question and receive a single response")
def ask(request: QuestionRequest):
    result = graph.invoke(
        {
            "session_id": request.session_id,
            "question": request.question,
        },
        config={"configurable": {"thread_id": request.session_id}},
    )
    return {"answer": result["answer"]}


@app.post("/ask_stream", summary="Ask a question and receive a streamed response")
def ask_stream(request: QuestionRequest):
    return StreamingResponse(event_generator(request), media_type="text/plain")


@app.get("/documents", summary="List all uploaded document names")
def get_all_documents():
    return get_documents()


@app.delete("/documents/{file_name}", summary="Delete all chunks for a document")
def remove_document(file_name: str):
    delete_documents(file_name)           
    delete_from_vector_store(file_name)   
    return {"message": f"{file_name} deleted successfully."}


@app.post("/summarize", summary="Generate a summary of an uploaded document")
def summarize(request: SummaryRequest):
    content = get_document_content(request.file_name)
    summary = summarize_document(content)
    return {"summary": summary}
