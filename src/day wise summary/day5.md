# Day 5: Text-to-SQL Agent

Welcome to Day 5 of the Domain-Specific RAG System for Cricket Analytics sprint! Today, we brought intelligent querying to our structured data by building a Text-to-SQL agent.

## What We Accomplished Today

1. **Environment Setup**
   - We installed `langchain-openai` and `python-dotenv` to enable querying via an LLM.
   - We created an `.env.example` file to securely store our `OPENAI_API_KEY`, setting the foundation for LLM-powered operations without hardcoding credentials into the source code.

2. **SQL Agent Implementation**
   - We created `src/sql_agent.py` to bridge natural language and our `cricket.db` SQLite database.
   - Using LangChain's `SQLDatabase` utility and `create_sql_agent`, we set up an agent powered by OpenAI's `gpt-3.5-turbo` model.
   - This agent is capable of examining the database schema (matches, players, ball_by_ball tables), forming a syntactically correct SQL query based on a user's prompt, executing it, and summarizing the result in plain English.

3. **Testing Logic**
   - Included a test block at the bottom of the script that simulates a user asking *"How many matches did India win?"*, with fallback logic providing a helpful warning if the API key isn't present in the `.env` file.

## Next Steps (Day 6)
With both Vector Retrieval (Day 4) and the SQL Agent (Day 5) fully implemented, we have our two main intelligence "tools". On Day 6, we will build **The Query Router**—an intelligent module that intercepts a user's prompt and decides whether to route it to the Vector Database (for match reports) or the SQL Agent (for hard statistics).
