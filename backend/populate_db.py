from embedding import embedding
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
import cfg
from langchain.storage import InMemoryStore
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import data_manage as data_manage
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
import calculate_retriver
# def fill_db(prompt):
#     docs=data_manage.data_up()
#     retriever=add_to_chroma(docs=docs,prompt=prompt)
#     return retriever



# def add_to_chroma(docs: list[Document],prompt):
#     # This text splitter is used to create the child documents
#     child_splitter = RecursiveCharacterTextSplitter(chunk_size=200,
#         chunk_overlap=30,
#         length_function=len,
#         is_separator_regex=False,)
# # The vectorstore to use to index the child chunks
#     vectorstore = Chroma(
#     collection_name="full_documents", embedding_function=embedding()
# )
# # The storage layer for the parent documents
#     store = InMemoryStore()
#     retriever = ParentDocumentRetriever(
#             vectorstore=vectorstore,
#             docstore=store,
#             child_splitter=child_splitter,
# )   
#     print("here")
#     retriever.add_documents(docs, ids=None)
#     list(store.yield_keys())
#     # sub_docs = vectorstore.similarity_search(query="project design")
#     # print(sub_docs[0].page_content)
#     retrieved_docs = retriever.invoke(prompt)
#     len(retrieved_docs[0].page_content)
#     return retriever
    # print("len(retrieved_docs[0].page_content)", len(retrieved_docs[0].page_content))
    # print("retrieved_docs[0].page_content", retrieved_docs[0].page_content)
    # print('here')
    # db=Chroma(persist_directory=cfg.db,embedding_function=embedding())
    
    # chunks_with_id=calculate_chunk_id(chunks)
    
    # exisiting_items=db.get(include=[])
    # exisiting_ids=set(exisiting_items['ids'])
    
    # new_chunks : list[Document] =[]
    # for chunk in chunks_with_id:
    #     if chunk.metadata['id'] not in exisiting_ids:
    #         new_chunks.append(chunk)
    
    # new_chunks_ids=[chunk.metadata['id'] for chunk in new_chunks]
    # db.add_documents(new_chunks,ids=new_chunks_ids)
    

    
        
    
# def calculate_chunk_id(chunks: list[Document]):
#     last_page_id=None
#     curent_chunk_index=0
    
#     for chunk in chunks:
#         source=chunk.metadata.get('source')
#         page=chunk.metadata.get('page')
#         current_page_id=f"{source}{page}"\
        
#         if current_page_id==last_page_id:
#             curent_chunk_index+=1
#         else:
#             curent_chunk_index=0
        
#         chunk_id=f"{current_page_id}{curent_chunk_index}"
        
#         last_page_id=current_page_id
#         chunk.metadata['id']=chunk_id
    
#     return chunks
    
def clear_database():
    db=Chroma(persist_directory=cfg.db,embedding_function=embedding())
    db.delete_collection()


