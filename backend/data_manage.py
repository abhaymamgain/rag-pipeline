from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import cfg



def load_documents():
    document_loader = PyPDFDirectoryLoader(cfg.PATH)
    return document_loader.load()


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)
def data_up():
    documents=load_documents()
    chunks=split_documents(documents)
    print(chunks[0])
    return chunks
 

   
