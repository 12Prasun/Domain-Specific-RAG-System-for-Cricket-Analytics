import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

def get_vectorstore():
    """Initializes and returns the Chroma vector store."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="cricket_reports"
    )
    return vectorstore

def get_retriever(k=5):
    """Returns a retriever object for the Chroma vector database."""
    vectorstore = get_vectorstore()
    
    # Configure the retriever to fetch top 'k' relevant chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever

if __name__ == "__main__":
    retriever = get_retriever()
    query = "Who won the T20 World Cup in 2022?"
    print(f"Testing query: '{query}'")
    
    docs = retriever.invoke(query)
    
    if docs:
        print(f"Found {len(docs)} documents.")
        for i, doc in enumerate(docs):
            print(f"\n--- Result {i+1} ---")
            print(doc.page_content)
            print("Metadata:", doc.metadata)
    else:
        print("No documents found. Please ensure the database is populated.")
