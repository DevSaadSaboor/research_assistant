import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.rag.loader import load_document, chunk_documents
from app.rag.store import create_vector_store, get_retriever
from app.rag.generator import generate_answer

FILE_PATH = "uploads/your-document.pdf"


def main() -> None:
    print(" Loading and indexing document...")
    documents = load_document(FILE_PATH)
    chunks = chunk_documents(documents)
    create_vector_store(chunks)
    retriever = get_retriever()

    print(" Document ready. Type your question or press Ctrl+C to quit.\n")

    while True:
        try:
            question = input("Ask Question: ").strip()
            if not question:
                continue

            retrieved_docs = retriever.invoke(question)
            context = "\n\n".join(doc.page_content for doc in retrieved_docs)
            answer = generate_answer(question, context)

            print(f"\nAnswer:\n{answer}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()
