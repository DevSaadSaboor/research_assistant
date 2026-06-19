import json
from typing import Generator

from app.graph.builder import graph

_SOURCES_MARKER = "\n\n__SOURCES__:"


def event_generator(request) -> Generator[str, None, None]:
    config = {"configurable": {"thread_id": request.session_id}}
    sources: list = []

    for chunk in graph.stream(
        {
            "session_id": request.session_id,
            "question": request.question,
        },
        config=config,
        stream_mode=["messages", "updates"],
    ):
        mode, data = chunk[0], chunk[1]

        if mode == "updates" and isinstance(data, dict) and "generate" in data:
            node_sources = data["generate"].get("sources")
            if node_sources is not None:
                sources = node_sources

        elif mode == "messages":
            message  = data[0] if isinstance(data, (list, tuple)) else data
            metadata = data[1] if isinstance(data, (list, tuple)) and len(data) > 1 else {}

            if (isinstance(metadata, dict)
                    and metadata.get("langgraph_node") == "generate"
                    and hasattr(message, "content")
                    and message.content):
                yield message.content

    if sources:
        yield _SOURCES_MARKER + json.dumps(sources)
