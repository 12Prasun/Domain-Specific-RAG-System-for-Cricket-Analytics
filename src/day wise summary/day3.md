# Day 3: Vector Database Setup

Welcome to Day 3 of the Domain-Specific RAG System for Cricket Analytics sprint! Today, we laid the foundation for processing unstructured data by integrating a Vector Database.

## What We Accomplished Today

1. **Simulating Unstructured Data**
   - Since we didn't have match reports, we successfully implemented a two-pronged approach to create our unstructured corpus.
   - First, we extracted 500 match summaries directly from our SQLite `matches` table and dynamically generated prose/text sentences out of them.
   - Second, we used the `wikipedia` Python package to seamlessly scrape articles covering major T20 events (like the 2022 and 2024 ICC Men's T20 World Cups).

2. **Chunking and Embedding**
   - We utilized LangChain's `RecursiveCharacterTextSplitter` to intelligently chunk our gathered text into bite-sized segments (1000 characters each).
   - We leveraged an offline, free HuggingFace Embedding model (`all-MiniLM-L6-v2`) to compute semantic vector representations of all 591 text chunks.

3. **Populating ChromaDB**
   - We initialized a persistent Chroma vector database locally at `data/chroma_db/`.
   - All 591 embedded chunks were successfully saved and made ready for vector search operations.

4. **Verification**
   - We ran a successful test vector retrieval querying "Who won the T20 World Cup in 2022?". The database accurately returned the chunk describing England's victory over Pakistan.

## Next Steps (Day 4)
With both our relational database (SQLite) and our vector database (Chroma) populated, Day 4 will revolve around building the actual LangChain/LlamaIndex code to reliably retrieve these text chunks in a production-ready manner!
