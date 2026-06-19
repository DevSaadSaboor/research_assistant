from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, Text, DateTime, distinct, Index
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url)
session_local = sessionmaker(bind=engine)
Base = declarative_base()



class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    file_name = Column(Text, nullable=False)
    chunk_text = Column(Text, nullable=False)


class Message(Base):
    __tablename__ = "messages"

    id         = Column(Integer, primary_key=True)
    session_id = Column(Text, nullable=False, index=True)  # indexed for fast history lookup
    role       = Column(Text, nullable=False)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)




def get_document_content(file_name: str) -> str:
    session = session_local()
    try:
        docs = (
            session.query(Documents)
            .filter(Documents.file_name == file_name)
            .all()
        )
        return "\n\n".join(doc.chunk_text for doc in docs)
    finally:
        session.close()


def get_documents() -> list[dict]:
    session = session_local()
    try:
        rows = session.query(distinct(Documents.file_name)).all()
        return [{"file_name": row[0]} for row in rows]
    finally:
        session.close()


def delete_documents(file_name: str) -> None:
    session = session_local()
    try:
        session.query(Documents).filter(Documents.file_name == file_name).delete()
        session.commit()
    finally:
        session.close()


def store_document_chunks(file_name: str, chunks: list) -> None:
    session = session_local()
    try:
        # Deduplication guard — remove stale chunks before re-inserting
        session.query(Documents).filter(Documents.file_name == file_name).delete()
        for chunk in chunks:
            doc = Documents(
                file_name=file_name,
                chunk_text=chunk.page_content,
            )
            session.add(doc)
        session.commit()
    finally:
        session.close()



def save_message(session_id: str, role: str, content: str) -> None:
    session = session_local()
    try:
        msg = Message(
            session_id=session_id,
            role=role,
            content=content,
            created_at=datetime.now(timezone.utc),
        )
        session.add(msg)
        session.commit()
    finally:
        session.close()


def load_messages(session_id: str) -> list[dict]:
    session = session_local()
    try:
        messages = (
            session.query(Message)
            .filter(Message.session_id == session_id)
            .order_by(Message.created_at)
            .all()
        )
        return [{"role": m.role, "content": m.content} for m in messages]
    finally:
        session.close()
