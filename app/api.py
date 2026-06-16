from fastapi import FastAPI,UploadFile, File
from .loader import load_document,chunk_documents
from .rag import create_vector_store
from .graph import graph
from pydantic import BaseModel
import os
DATABASE_URL =  os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is missing from .env")
app = FastAPI()


@app.post("/upload")
def upload(file:UploadFile = File(...)):
    file_path = f"documents/{file.filename}"
    with open(file_path,"wb") as buffer:
        buffer.write(file.file.read())
    documents = load_document(file_path)
    chunks = chunk_documents(documents)
    vector_store = create_vector_store(chunks,DATABASE_URL)
    return {
        "message" : "document uploaded successfully"
    }

class QuestionRequest(BaseModel):
    question:str


@app.post("ask")
def ask(request:QuestionRequest):
    result = graph.invoke({
        "session_id": request.session_id,
        "question":request.question
    }
    config= {
         "configurable": {
                "thread_id":
                    request.session_id
            }
    })
    
    return {
        "answer":result["answer"]
    }

