from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import yaml

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../settings/config.yml')), 'r') as config_file:
    config = yaml.safe_load(config_file)
    RAGEmbeddingModel = config.get('RAGEmbeddingModel', 'mistral')

class Retriever():
    def __init__(self, name: str = "Tucker", type: str = "Golden") -> None:
        self.name = name
        self.type = type + " retriever"
        self.retriever = None
    
    def __str__(self) -> str:
        return str(self.name)
    
    def __type__(self):
        return str(self.type)
    
    def hide(self, splits) -> None:
        embeddings = OllamaEmbeddings(model=RAGEmbeddingModel)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        self.retriever = vectorstore.as_retriever()
    
    def chew(self, docs) -> list:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return text_splitter.split_documents(docs)

    def fetch(self, question):
        fetched_docs = self.retriever.invoke(question)
        return self.format(fetched_docs)
    
    def format(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
