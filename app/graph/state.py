from typing import TypedDict


class GraphState(TypedDict):
    """
    Shared state passed between every node in the LangGraph agent.

    Fields:
        session_id:   Unique ID for the conversation (used for memory + checkpointing).
        question:     The user's input question.
        answer:       The generated answer (populated by generate_node).
        context:      Retrieved document chunks (populated by retrieve_node).
        sources:      Citation metadata for the retrieved chunks [{file_name, page, preview}].
        messages:     Conversation history loaded from the database.
        is_relevant:  Whether retrieved context is sufficient (set by grade_retrieval_node).
        web_context:  Web search results (populated by web_search_node when needed).
    """

    session_id: str
    question: str
    answer: str
    context: str
    sources: list
    messages: list
    is_relevant: bool
    web_context: str
