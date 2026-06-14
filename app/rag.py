from langchain_openai import OpenAIEmbeddings,ChatOpenAI


def create_embedding(chunks):
    embedding_model = OpenAIEmbeddings()
    texts = [chunk.page_content for chunk in chunks]
    vectors = embedding_model.embed_documents(texts)
    
    embedded_chunks = []
    for chunk, vector in zip(chunks, vectors):
        embedded_chunks.append({
            "chunk_text": chunk.page_content,
            "embedding": vector
        })
    return embedded_chunks

def generate_answer(question,context):
    llm = ChatOpenAI(model = "gpt-4o-mini")

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