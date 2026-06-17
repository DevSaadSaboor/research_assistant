from langgraph.graph import StateGraph, END, START
from app.graph.state import GraphState
from app.graph.checkpoint import checkpointer
from app.graph.edges import routing_after_grading
from app.graph.nodes import (
    load_history_node,
    retrieve_node,
    grade_retrieval_node,
    web_search_node,
    generate_node,
    save_messages_node,
)

_builder = StateGraph(GraphState)

_builder.add_node("load_history",load_history_node)
_builder.add_node("retrieve",retrieve_node)
_builder.add_node("grade_retrieval",grade_retrieval_node)
_builder.add_node("web_search",web_search_node)
_builder.add_node("generate",generate_node)
_builder.add_node("save_messages",save_messages_node)


_builder.add_edge(START,"load_history")
_builder.add_edge("load_history","retrieve")
_builder.add_edge("retrieve","grade_retrieval")

_builder.add_conditional_edges(
    "grade_retrieval",
    routing_after_grading,
    {
        "generate":   "generate",
        "web_search": "web_search",
    },
)

_builder.add_edge("web_search","generate")
_builder.add_edge("generate","save_messages")
_builder.add_edge("save_messages",END)


graph = _builder.compile(checkpointer=checkpointer)
