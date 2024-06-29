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

import embedding as embedding
import llm_calls as lc
import cfg
import calculate_retriver

def prompt_func(dict):
    format_texts = "\n".join(dict["context"])
    
    content=[
                {"type": "text", "text": f"""Answer the question based only on the following context, 
                 which can include text, tables,images
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
    
    retriever =calculate_retriver.get_calculated_variable()
    
    
    
    
    # docs =retriever.get_relevant_documents('what is the trend in the Dow jones chart')
    # print(len(docs))
    # doctype=split_image_text_types(docs)
    # print(doctype['images'][:])
    # print('=='*30)
    # print(doctype['texts'][0])
    
        
# RAG pipeline
    chain = (
        {"context": retriever , "question": RunnablePassthrough()}
        |{"context":RunnableLambda(LongContextReorder.transform_documents),"question": RunnablePassthrough()}
        | RunnableLambda(prompt_func)
        | RunnableLambda(lc.llm_generate)
        | StrOutputParser()
        )

    response=chain.invoke(prompt)
    print(response)
    return response
