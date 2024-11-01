from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Retriever():
    def __init__(self, RAGEmbeddingModel: str = 'mistral', **kwargs) -> None:
        self.RAGEmbeddingModel: str = RAGEmbeddingModel
        self.retriever = None
        
        #! Not important just for the joke
        self.name = kwargs.get('name', "Tucker")
        self.type = kwargs.get('type', "Golden") + " Retriever"
    
    def __str__(self) -> str:
        return str(self.name)
    
    def __type__(self):
        return str(self.type)
    
    def hide(self, splits) -> None:
        embeddings = OllamaEmbeddings(model=self.RAGEmbeddingModel)
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
