from embedding import embedding
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import cfg
# import torch
# Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
# import transformers
# import os
from langchain_community.llms.ollama import Ollama


def query_rag(query_text:str):
    
    
    
    
    
    
    embedding_func=embedding()
    db_chroma=Chroma(
        embedding_function=embedding_func,
        persist_directory=cfg.db
    )
    
    PROMT_TEMPLATE="""Answer the question based only on following context
    {context}
    
    --------
    answer this question based on the context above:{question}
    
    
    """
    results=db_chroma.similarity_search_with_score(query_text,k=5)
    
    context_text="\n\n---\n\n".join([doc.page_content for doc, _score in results])
    promt_template=ChatPromptTemplate.from_template(PROMT_TEMPLATE)
    prompt = promt_template.format(context=context_text,question=query_text)
    print(prompt)
    
    # login(token='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')
    # os.environ['HF_TOKEN']='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'
    # os.environ['HUGGINGFACEHUB_API_TOKEN']='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'
    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    #model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
    #text_generator = transformers.pipeline("text-generation", model=model_name, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto",pad_token_id=tokenizer.eos_token_id)
    
    model=Ollama(
                 model='llama3')
    response_text=model.invoke(prompt,max_length=100)
    
    print('REACHED')
    print(response_text)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


