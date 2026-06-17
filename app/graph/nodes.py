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
    return {"context": context}


def grade_retrieval_node(state: GraphState) -> dict:
    prompt = f"""
    Question:
    {state["question"]}

    Retrieved Chunks:
    {state["context"]}

    Determine whether the retrieved context contains enough information
    to answer the question.
    Return only: yes or no
    """
    result = model.invoke(prompt)
    return {"is_relevant": result.content.strip().lower() == "yes"}


def web_search_node(state: GraphState) -> dict:
    result = search_tool.invoke(state["question"])
    return {"web_context": result}


def generate_node(state: GraphState) -> dict:
    messages = state.get("messages", [])
    context = state["context"] if state["is_relevant"] else state.get("web_context", "")

    history = "".join(
        f"{m['role']}: {m['content']}\n"
        for m in messages
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
    return {"answer": result.content}


def save_messages_node(state: GraphState) -> dict:
    save_message(state["session_id"], "user", state["question"])
    save_message(state["session_id"], "assistant", state["answer"])
    return {}
