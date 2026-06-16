from typing import TypedDict
from langgraph.graph import  StateGraph,END,START
from .rag import get_retriever
from .checkpoint import checkpointer
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")
retriever = get_retriever()


class GraphState(TypedDict):
    session_id:str
    question:str
    answer:str
    context:str
    messages:list

def load_message(state:GraphState):
    session_id = state["session_id"]
    messages = load_message(session_id)
    return {
        "messages": messages
    }

def retreive_node(state:GraphState):
    question = state["question"]
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)
    return {
        "context":context
    }

def save_message(state:GraphState):
    question = state["question"]
    answer = state["answer"]
    session_id = state["session_id"]

    save_message(session_id,"user",question)
    save_message(session_id,"assistant",answer)
    return {}


def generate_node(state:GraphState):
    question = state["question"]
    context = state["context"]
    prompt = f"""
    You are a Research Assistant 
    Answer the question based on the Given context:
    if you dont know the answer return "I dont know the answer bases on context" 
    Context:
    {context}
    Question:
    {question}
    """

    result = model.invoke(prompt)
    return {
        "answer": result.content
    }


graph_builder = StateGraph(GraphState)

graph_builder.add_node("load_history", load_message)
graph_builder.add_node("retrieve", retreive_node)
graph_builder.add_node("save_messages", save_message)
graph_builder.add_node("generate",generate_node)
graph_builder.add_edge(START,"load_history")
graph_builder.add_edge("load_history","retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate","save_messages")
graph_builder.add_edge("save_messages", END)

graph = graph_builder.compile(checkpointer=checkpointer)
    

