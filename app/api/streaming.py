from typing import Generator
from app.graph.builder import graph

def event_generator(request) -> Generator[str, None, None]:
    for message, metadata in graph.stream(
        {
            "session_id": request.session_id,
            "question": request.question,
        },
        config={
            "configurable": {
                "thread_id": request.session_id,
            }
        },
        stream_mode="messages",
    ):
        if message.content and metadata.get("langgraph_node") == "generate":
            yield message.content
