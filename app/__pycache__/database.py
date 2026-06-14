from sqlalchemy import (create_engine,Column,Integer,Text)
from sqlalchemy.orm import (declarative_base,sessionmaker)
from pgvector.sqlalchemy import Vector
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv
DATABASE_URL =  os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is missing from .env")

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(bind=engine)

Base = declarative_base()

class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer,primary_key=True)
    file_name = Column(Text,nullable=False)
    chunk_text = Column(Text,nullable=False)
    embedding = Column(Vector(1536))


Base.metadata.create_all(bind= engine)


def store_in_database(file_name,embedding_chunks):

    session = session_local()
    try:
        for item in embedding_chunks:
            documents = Documents(
                file_name=file_name,
                chunk_text=item["chunk_text"],
                embedding = item["embedding"]
            )
            session.add(documents)
        session.commit()
    
    finally:
        session.close()


def retrieve_content(question):
    embedding_model = OpenAIEmbeddings()
    question_embedding = embedding_model.embed_query(question)
    session = session_local()

    try:
        results = (session.query(Documents).order_by(Documents.embedding.cosine_distance(question_embedding)).limit(5).all())
        chunks = [result.chunk_text for result in results]
        content = "\n\n".join(chunks)
        return content
    
    finally:
        session.close()


    