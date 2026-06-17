from langgraph.checkpoint.postgres import PostgresSaver
from app.core.config import settings

_checkpointer_ctx = PostgresSaver.from_conn_string(settings.database_url)
checkpointer = _checkpointer_ctx.__enter__()


def setup_checkpointer() -> None:
    checkpointer.setup()


def shutdown_checkpointer() -> None:
    _checkpointer_ctx.__exit__(None, None, None)
