# Day 4: Basic Vector Retrieval

Welcome to Day 4 of the Domain-Specific RAG System for Cricket Analytics sprint! Today, we successfully built the vector retrieval logic to query the text chunks stored in ChromaDB.

## What We Accomplished Today

1. **Retrieval Setup**
   - Created `src/retriever.py` to instantiate our HuggingFace embedding model (`all-MiniLM-L6-v2`) and connect to the local `data/chroma_db/`.
   - Built a `get_retriever()` function that returns a LangChain retriever interface configured to fetch the top 5 most relevant documents (`k=5`).

2. **Testing and Verification**
   - Wrote a test script block at the end of the file to query the database with a natural language question ("Who won the T20 World Cup in 2022?").
   - Verified that the retriever successfully fetches matching synthetic match reports and Wikipedia chunks from our offline corpus.

## Next Steps (Day 5)
Now that our unstructured vector retrieval is operational, we will shift gears to the structured side. On Day 5, we will build a Text-to-SQL agent using LangChain, allowing us to generate accurate SQL queries from natural language to query our SQLite tables!
