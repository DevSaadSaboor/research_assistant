import os 
from langgraph.checkpoint.postgres import PostgresSaver
DATABASE_URL =  os.getenv("DATABASE_URL")
checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)


with checkpointer as cp:
    cp.setup()