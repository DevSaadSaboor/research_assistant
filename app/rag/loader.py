from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    return splitter.split_documents(documents)
