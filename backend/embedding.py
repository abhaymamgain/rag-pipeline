from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

def embedding():
    embedded=FastEmbedEmbeddings()
    return embedded