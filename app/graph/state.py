from typing import TypedDict

class GraphState(TypedDict):
    session_id: str
    question: str
    answer: str
    context: str
    messages: list
    is_relevant: bool
    web_context: str
