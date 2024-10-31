import ollama
from langchain_community.document_loaders import WebBaseLoader

from retriver import Retriever

tucker = Retriever(name="Tucker", type="Golden")

loader = WebBaseLoader(
    web_paths=("https://en.wikipedia.org/wiki/Europa_Clipper",),
)
docs = loader.load()
splits = tucker.chew(docs)

# Create Ollama embeddings and vector store
tucker.hide(splits)

# Define Ollama LLM function
def ollama_llm(question, context):
    formatted_prompt = f"Question: {question}\n\nContext: {context}"
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": formatted_prompt}])
    return response['message']['content']

# Define RAG chain
def rag_chain(question):
    context = tucker.fetch(question)
    return ollama_llm(question, context)

# Run the RAG chain
result = rag_chain("What is the Europa Clipper?")
print(result)