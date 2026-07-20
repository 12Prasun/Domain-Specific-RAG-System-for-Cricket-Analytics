import os
import sqlite3
import wikipedia
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "cricket.db")
CHROMA_PATH = os.path.join(BASE_DIR, "data", "chroma_db")

def get_synthetic_match_reports(limit=50):
    """Generate synthetic match reports from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT date, venue, team1, team2, toss_winner, toss_decision, winner FROM matches LIMIT ?", (limit,))
    matches = cursor.fetchall()
    conn.close()
    
    reports = []
    for match in matches:
        date, venue, team1, team2, toss_winner, toss_decision, winner = match
        if not date or not venue or not team1 or not team2:
            continue
        report = (
            f"On {date}, a T20 match was played between {team1} and {team2} at {venue}. "
            f"The toss was won by {toss_winner}, who decided to {toss_decision}. "
            f"Ultimately, {winner} emerged victorious in this exciting contest."
        )
        reports.append(Document(page_content=report, metadata={"source": "database_synthesis", "type": "match_summary"}))
    return reports

def get_wikipedia_articles(queries=["2022 ICC Men's T20 World Cup", "2024 ICC Men's T20 World Cup", "Indian Premier League"]):
    """Fetch text content from Wikipedia articles."""
    docs = []
    for query in queries:
        try:
            print(f"Fetching Wikipedia article: {query}")
            page = wikipedia.page(query)
            docs.append(Document(page_content=page.content, metadata={"source": "wikipedia", "title": page.title}))
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    return docs

def setup_vector_db():
    print("Gathering text data...")
    docs = []
    docs.extend(get_synthetic_match_reports(limit=500))
    docs.extend(get_wikipedia_articles())
    
    print(f"Gathered {len(docs)} documents. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Created {len(chunks)} text chunks.")
    
    print("Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Creating Chroma vector store...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name="cricket_reports"
    )
    vectorstore.persist()
    print(f"Successfully created and persisted ChromaDB at {CHROMA_PATH}")

if __name__ == "__main__":
    setup_vector_db()
