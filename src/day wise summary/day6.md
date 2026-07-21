# Day 6: The Query Router

Welcome to Day 6 of the Domain-Specific RAG System for Cricket Analytics sprint! Today, we built the "brain" of our hybrid architecture—The Query Router.

## What We Accomplished Today

1. **Intelligent Routing Logic**
   - We created `src/query_router.py`. This script introduces a `route_query()` function that leverages LangChain and an LLM (`gpt-3.5-turbo`) to classify a natural language prompt.
   - The router is prompted to respond with exactly "sql" (if the query relates to hard statistics, match outcomes, or counting) or "vector" (if it asks for summaries, history, or textual prose).

2. **End-to-End Pipeline (`process_query`)**
   - We implemented the main `process_query()` function to unify our Day 4 and Day 5 work.
   - If routed to **SQL**: The function automatically invokes the LangChain SQL Agent to write and execute a query against SQLite.
   - If routed to **Vector**: The function hits ChromaDB, retrieves the top 3 relevant chunks, and then uses a custom RAG prompt chain to synthesize a cohesive answer from the unstructured data.

3. **Testing the Hybrid System**
   - We set up a test suite to automatically process a mixed bag of questions (e.g., *"Who won the T20 World Cup in 2022?"* vs. *"How many matches are recorded in our database?"*). The router accurately intercepts the requests, directs them to the correct backend tool, and delivers seamless answers!

## Next Steps (Day 7)
Day 7 marks the end of Week 1! We will take the day to step back, clean up our code, resolve any looming bugs or deprecation warnings, and ensure the entire backend CLI runs flawlessly before we dive into Advanced Logic and UI components in Week 2!
