# Domain-Specific RAG System for Cricket Analytics: 14-Day Sprint Plan

**Project Owner:** Prasun
**Core Technologies:** Python, LangChain/LlamaIndex, ChromaDB, SQLite, Streamlit

## Project Context
Building a hybrid RAG system that processes both unstructured text (cricket match reports/commentary via ChromaDB) and structured hard statistics (historical ball-by-ball data via SQLite). It will feature sports-specific Entity Recognition (NER), an LLM router to choose between vector search and SQL execution, and a Streamlit UI.

## Rules of Engagement
1. **One Day at a Time:** Strictly follow the 14-day plan below. 
2. **Modular Code:** Write production-grade, modular Python code (e.g., separate files for `database.py`, `retriever.py`, `llm_router.py`).
3. **Strict Git Workflows:** End every task with Conventional Commits (e.g., `feat: setup SQLite schema for player stats`).

## The 14-Day Sprint Plan

### Week 1: Data Pipelines & Core RAG
* **Day 1: Repository Setup & Data Ingestion.** Initialize Git repository, set up virtual environment, and download historical JSON/CSV data from Cricsheet.
* **Day 2: Relational Database Setup.** Create a local SQLite database, design the schema (players, matches, ball_by_ball), and write a Python script to populate it with Cricsheet data.
* **Day 3: Vector Database Setup.** Write a script to scrape or process text data (match reports) and embed them into a local ChromaDB instance.
* **Day 4: Basic Vector Retrieval.** Implement the LangChain/LlamaIndex code to retrieve relevant text chunks from ChromaDB based on a user query.
* **Day 5: Text-to-SQL Agent.** Implement a LangChain SQL Agent that translates natural language queries into accurate SQL queries.
* **Day 6: The Query Router.** Build the logic that takes a user prompt and decides whether to route it to the Vector DB or the SQL Database.
* **Day 7: Buffer & Refactor.** Clean up code, fix week 1 bugs, and ensure the backend works seamlessly via terminal commands.

### Week 2: Advanced Logic, Live Data, & UI
* **Day 8: Sports-Specific NER.** Implement custom extraction logic to identify cricket entities (e.g., recognizing "googly" maps to a spin bowling classification).
* **Day 9: Statistical Reasoning Logic.** Implement a Python function to calculate complex custom metrics (like a weighted "Player Performance Index"). The mathematical optimization techniques you apply in your engineering coursework will be highly valuable for structuring these algorithmic proofs and dynamic weights.
* **Day 10: Live Data Integration.** Integrate a free Cricket API (like CricAPI) to fetch today's live match scores.
* **Day 11: Streamlit UI (Part 1).** Build the frontend layout using Streamlit.
* **Day 12: Streamlit UI (Part 2).** Add data visualizations directly into the UI based on SQL data.
* **Day 13: Edge Case Testing.** Test the system with complex, adversarial queries.
* **Day 14: Documentation & Deployment.** Write a stellar, recruiter-ready `README.md` with architecture diagrams.

***

### How to Execute This Plan
Feed this plan to your AI assistant of choice and start with the following prompt:
> "Acknowledge these instructions. Then, guide me through **Day 1: Repository Setup & Data Ingestion**. Give me the exact terminal commands to set up the environment, the folder structure we will use, and the Python code to download our first batch of data. End your response with the Git commands to commit this initial setup."
