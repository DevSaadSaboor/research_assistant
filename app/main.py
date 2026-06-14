from dotenv import load_dotenv
load_dotenv()

from loader import (load_document,chunk_documents)
from rag import (create_embedding,generate_answer)
from database import (store_in_database,retrieve_content)

def ingest_document():

    file_path = "uploads/Lecture-AI.pdf"

    file_name = "ai_book.pdf"

    documents = load_document(file_path)

    chunks = chunk_documents(
        documents
    )

    embedded_chunks = create_embedding(
        chunks
    )

    store_in_database(
        file_name=file_name,
        embedding_chunks=embedded_chunks
    )

    print("Document Stored Successfully")


def ask_question():

    question = input(
        "Ask Question: "
    )

    context = retrieve_content(
        question
    )

    answer = generate_answer(
        question=question,
        context=context
    )

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":

    ingest_document()

    while True:

        ask_question()