from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from app.core.config import settings
embedding = OpenAIEmbeddings(api_key=settings.openai_api_key)


def create_vector_store(chunks, connection_string: str | None = None):
    conn = connection_string or settings.database_url
    vector_store = PGVector.from_documents(
        documents=chunks,
        embedding=embedding,
        collection_name="research_documents",
        connection=conn,
    )
    return vector_store


def delete_from_vector_store(file_name: str) -> None:
    """
    Remove all embeddings for a document from the PGVector collection.

    PGVector stores embeddings in langchain_pg_embedding. Each row carries
    a 'cmetadata' JSON column that includes 'source' (the file path set by
    PyPDFLoader). We match on file_name as a suffix so the lookup is
    path-independent.
    """
    from sqlalchemy import create_engine, text

    engine = create_engine(settings.database_url)
    with engine.connect() as conn:
        conn.execute(
            text("""
                DELETE FROM langchain_pg_embedding
                WHERE collection_id = (
                    SELECT uuid FROM langchain_pg_collection
                    WHERE name = 'research_documents'
                )
                AND cmetadata->>'source' LIKE :pattern
            """),
            {"pattern": f"%{file_name}"},
        )
        conn.commit()


def get_retriever():
    vector_store = PGVector(
        embeddings=embedding,
        collection_name="research_documents",
        connection=settings.database_url,
    )
    return vector_store.as_retriever(search_kwargs={"k": 5})
