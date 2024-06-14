from langchain.schema.document import Document
from embedding import embedding
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import cfg
from langchain_community.document_transformers import LongContextReorder
from huggingface_hub import login
from langchain_community.llms.ollama import Ollama


def Hypo_doc_generator(query_text):
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
    # results=LongContextReorder().transform_documents(results)
    
    context_text="\n\n---\n\n".join([doc.page_content for doc,_score in results])
    promt_template=ChatPromptTemplate.from_template(PROMT_TEMPLATE)
    prompt = promt_template.format(context=context_text,question=query_text)
    print(prompt)
    
    # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    #model = AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
    #text_generator = transformers.pipeline("text-generation", model=model_name, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto",pad_token_id=tokenizer.eos_token_id)
    
    model=Ollama(
                 model='llama3')
    response_text=model.invoke(prompt,max_length=200)
    
    print('REACHED')
    print(response_text)
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    response_doc=Document(page_content=response_text,metadatas={'source':'hypothetical1','page':'0'})
    return response_doc,response_text