from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_document(file_path):
    loader = PyPDFLoader(file_path)
    document = loader.load()
    return document

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 30
    )
    chunk  = splitter.split_documents(documents)
    return chunk




    


