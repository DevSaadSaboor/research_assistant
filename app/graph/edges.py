from app.graph.state import GraphState


def routing_after_grading(state: GraphState) -> str:
    return "generate" if state["is_relevant"] else "web_search"
