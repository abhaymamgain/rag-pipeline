import os
from unstructured.partition.pdf import partition_pdf
import cfg
import llm_calls as lc
from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.vectorstores.chroma import Chroma
from langchain.schema.document import Document
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
import uuid
import embedding as embedding
from image_processing import image_capt_summary_list
import calculate_retriver
# Directory containing PDF files
pdf_directory = cfg.PATH

# Function to partition the PDF and process sections
def doc_partition(path,file_name):
  raw_pdf_elements = partition_pdf(
    filename=path +'/' +file_name,
    extract_images_in_pdf=True,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=10,
    image_output_dir_path='content')

  return raw_pdf_elements


def process_all_pdfs_in_directory(pdf_directory):
    raw_elements_list=[]
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
          raw_elements=doc_partition(pdf_directory,filename)
          raw_elements_list.extend(raw_elements)
          
    return   raw_elements_list    



def data_category(raw_pdf_elements): 
    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
           tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
           texts.append(str(element))
    data_category = [texts,tables]
    return data_category
  
def tables_summarize(tables):
    prompt_text = """You are an assistant tasked with summarizing tables. \
                    Give a concise summary of the table. Table chunk: {element} """

    prompt = ChatPromptTemplate.from_template(prompt_text)
    # model=Ollama(model='llava')
    summarize_chain = {"element": lambda x: x} | prompt | RunnableLambda(lc.llm_generate) | StrOutputParser()
    table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})
    

    return table_summaries  
  


def process_store():
    raw_pdf_elements=process_all_pdfs_in_directory(cfg.PATH)
  
    texts = data_category(raw_pdf_elements)[0]
    tables = data_category(raw_pdf_elements)[1]
    print(texts)
    print("="*20)
    print(tables)
    table_summaries=[]
    if tables:
        table_summaries=tables_summarize(tables)
    text_summaries=texts
    print("=="*20)
    print(table_summaries)

    vectorstore=Chroma(collection_name='multi-modal-rag',embedding_function=embedding.embedding(),persist_directory=cfg.db)
    store = InMemoryStore()
    id_key = "doc_id"
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key=id_key,
)

    doc_ids = [str(uuid.uuid4()) for _ in texts]
    summary_texts = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(text_summaries)
    ]

    retriever.vectorstore.add_documents(summary_texts)
    retriever.docstore.mset(list(zip(doc_ids, texts)))

# Add tables
    if tables:
        table_ids = [str(uuid.uuid4()) for _ in tables]
        summary_tables = [
        Document(page_content=s, metadata={id_key: table_ids[i]})
        for i, s in enumerate(table_summaries)
]
        retriever.vectorstore.add_documents(summary_tables)
        retriever.docstore.mset(list(zip(table_ids, tables)))
#add images
       
        img_base64_list,image_summaries=image_capt_summary_list(cfg.img)
        if img_base64_list:
            img_ids = [str(uuid.uuid4()) for _ in img_base64_list]
            summary_img = [
            Document(page_content=s, metadata={id_key: img_ids[i]})
            for i, s in enumerate(image_summaries)
    ]
            retriever.vectorstore.add_documents(summary_img)
            retriever.docstore.mset(list(zip(img_ids, summary_img)))
    
    calculate_retriver.set_calculated_variable(retriever)
    

    
