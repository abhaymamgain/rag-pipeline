from embedding import embedding
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
import cfg

import data_manage as data_manage

def fill_db():
    chunks=data_manage.data_up()
    add_to_chroma(chunks)



def add_to_chroma(chunks: list[Document]):
    db=Chroma(persist_directory=cfg.db,embedding_function=embedding())
    
    chunks_with_id=calculate_chunk_id(chunks)
    
    exisiting_items=db.get(include=[])
    exisiting_ids=set(exisiting_items['ids'])
    
    new_chunks : list[Document] =[]
    for chunk in chunks_with_id:
        if chunk.metadata['id'] not in exisiting_ids:
            new_chunks.append(chunk)
    
    new_chunks_ids=[chunk.metadata['id'] for chunk in new_chunks]
    db.add_documents(new_chunks,ids=new_chunks_ids)
    

    
        
    
def calculate_chunk_id(chunks: list[Document]):
    last_page_id=None
    curent_chunk_index=0
    
    for chunk in chunks:
        source=chunk.metadata.get('source')
        page=chunk.metadata.get('page')
        current_page_id=f"{source}{page}"\
        
        if current_page_id==last_page_id:
            curent_chunk_index+=1
        else:
            curent_chunk_index=0
        
        chunk_id=f"{current_page_id}{curent_chunk_index}"
        
        last_page_id=current_page_id
        chunk.metadata['id']=chunk_id
    
    return chunks
    
def clear_database():
    db=Chroma(persist_directory=cfg.db,embedding_function=embedding())
    db.delete_collection()
