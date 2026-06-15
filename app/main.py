from loader import (
    load_document,
    chunk_documents
)

from rag import (
    create_vector_store,
    get_retriever,
    generate_answer
)

import os 
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL")

file_path = "documents/ai_book.pdf"


documents = load_document(
    file_path
)

chunks = chunk_documents(
    documents
)

vector_store = create_vector_store(
    chunks,
    DATABASE_URL
)

retriever = get_retriever(
    vector_store
)


while True:

    question = input(
        "\nAsk Question: "
    )

    retrieved_docs = retriever.invoke(
        question
    )

    context = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    answer = generate_answer(
        question,
        context
    )

    print("\nAnswer:")
    print(answer)