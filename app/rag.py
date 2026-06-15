from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_postgres import PGVector
llm = ChatOpenAI(model = "gpt-4o-mini")
embedding = OpenAIEmbeddings()


def create_vector_store(chunks,connection_string):
    vector_store = PGVector.from_documents(documents=chunks,embedding=embedding,collection_name="research_documents", connection=connection_string)
    return vector_store


def get_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )
    return retriever    

def generate_answer(question,context):


    prompt = f"""
    You are AI assistant 
    Use only the provided context to answer the question
    Context:
    {context}
    Question:
    {question}
    """

    response = llm.invoke(prompt)
    return response.content


# def create_embedding(chunks):
#     embedding_model = OpenAIEmbeddings()
#     texts = [chunk.page_content for chunk in chunks]
#     vectors = embedding_model.embed_documents(texts)
    
#     embedded_chunks = []
#     for chunk, vector in zip(chunks, vectors):
#         embedded_chunks.append({
#             "chunk_text": chunk.page_content,
#             "embedding": vector
#         })
#     return embedded_chunks

