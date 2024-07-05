from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.messages import HumanMessage, SystemMessage
from partition import process_store
from langchain_community.llms.ollama import Ollama
from langchain.schema.output_parser import StrOutputParser
from image_processing import split_image_text_types
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_transformers import LongContextReorder
from hyde import Hypo_doc_generator
import embedding as embedding
import llm_calls as lc
import cfg
import calculate_retriver
from langchain.schema.document import Document
import populate_db

def prompt_func(dict):
    format_texts = "\n".join(dict["context"])
    print("dict[\"context\"]", dict["context"])
    
    content=[
                {"type": "text", "text": f"""
                 you do your job with maximum accuracy you will
                 Answer the question based on only the following context which might contain texts or tables, 
                 
                Question: {dict["question"]}

                Text and tables: {format_texts}
                
                """}
                # {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{dict['context']['images'][0]}"}},
                
            ]
    # if "images" in dict["context"] and dict["context"]["images"]:
    #             image_data = dict["context"]["images"][0]
    #             if not image_data.startswith("Input Parameter Values:"):
    #                 content.append({
    #                             "type": "image_url",
    #                             "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
    #                                 })
    return [
        HumanMessage(
            content=content
        )
    ]

    

def run(prompt):
    
    hypo_doc,gen_query=Hypo_doc_generator(prompt)
    print("hypo_doc,gen_query", hypo_doc,gen_query)
    hypo_doc_list: list[Document] = [hypo_doc]
    print("hypo_doc_list", hypo_doc_list)
    retriver = calculate_retriver.get_calculated_variable()
   
    
        
# RAG pipeline
    chain = (
        {"context": retriver , "question": RunnablePassthrough()}
        | RunnableLambda(prompt_func)
        | RunnableLambda(lc.llm_generate)
        | StrOutputParser()
        )

    response=chain.invoke(prompt)
    print(response)
    return response

