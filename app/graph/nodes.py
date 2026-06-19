import os

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from app.graph.state import GraphState
from app.rag.store import get_retriever
from app.core.database import load_messages, save_message
from app.core.config import settings

model = ChatOpenAI(model="gpt-4o-mini", streaming=True, api_key=settings.openai_api_key)
retriever = get_retriever()
search_tool = DuckDuckGoSearchResults()


def load_history_node(state: GraphState) -> dict:
    messages = load_messages(state["session_id"])
    return {"messages": messages}


def retrieve_node(state: GraphState) -> dict:
    docs = retriever.invoke(state["question"])
    context = "\n\n".join(doc.page_content for doc in docs)

    seen: set = set()
    sources: list = []
    for doc in docs:
        meta = doc.metadata
        raw_source = meta.get("source", "")
        file_name = os.path.basename(raw_source) if raw_source else "Unknown"
        page = meta.get("page", 0) + 1 
        key = (file_name, page)
        if key not in seen:
            seen.add(key)
            sources.append({
                "file_name": file_name,
                "page": page,
                "preview": doc.page_content[:120].strip() + "…",
            })

    return {"context": context, "sources": sources}


def grade_retrieval_node(state: GraphState) -> dict:
    context = state.get("context", "").strip()


    if len(context) < 50:
        return {"is_relevant": False}
    prompt = f"""Does the text below contain information that directly answers the question?

Question: {state["question"]}

Text:
{context[:2000]}

Reply with ONLY "yes" or "no".
"yes" = the text contains the specific information needed to answer the question.
"no"  = the text is about a different topic and cannot answer the question."""

    result = model.invoke(prompt)
    return {"is_relevant": result.content.strip().lower().startswith("yes")}


def web_search_node(state: GraphState) -> dict:
    result = search_tool.invoke(state["question"])
    return {"web_context": result}


def generate_node(state: GraphState) -> dict:
    is_relevant = state.get("is_relevant", False)
    messages    = state.get("messages", [])
    context     = state["context"] if is_relevant else state.get("web_context", "")

    sources = state.get("sources", []) if is_relevant else []

    # Limit history to last 10 messages to stay within token limits
    recent = messages[-10:] if len(messages) > 10 else messages
    history = "".join(
        f"{m['role']}: {m['content']}\n"
        for m in recent
    )

    prompt = f"""
    You are a Research Assistant.

    Conversation History:
    {history}

    Context:
    {context}

    Question:
    {state["question"]}

    Answer the question using only the provided context.
    """
    result = model.invoke(prompt)
    return {"answer": result.content, "sources": sources}


def save_messages_node(state: GraphState) -> dict:
    save_message(state["session_id"], "user", state["question"])
    save_message(state["session_id"], "assistant", state["answer"])
    return {}
