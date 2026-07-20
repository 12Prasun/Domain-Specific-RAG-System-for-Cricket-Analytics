# Day 2: Relational Database Setup

Welcome to Day 2 of the Domain-Specific RAG System for Cricket Analytics! Today, we successfully built the relational database component of our architecture.

## What We Accomplished Today

1. **Designed the Database Schema**
   - We created `src/database.py` to handle setting up a local SQLite database (`data/cricket.db`).
   - We designed three core tables: `matches`, `players`, and `ball_by_ball` to efficiently store the historical match data.

2. **Built the Ingestion Script**
   - We created `src/populate_db.py`, a script that iterates through all the raw JSON files downloaded from Cricsheet.
   - The script intelligently parses the deeply nested JSON structure and extracts relevant details like match metadata, player registry, and delivery-by-delivery outcomes.

3. **Populated the Database**
   - We ran the ingestion script across 5,550 JSON files!
   - This process populated our database with:
     - 5,550 Matches
     - 8,257 Players
     - Over 1.25 Million Deliveries!

## Next Steps (Day 3)
With our structured historical statistics safely stored and easily queryable in SQLite, we are ready to move on to unstructured text data. Day 3 will involve processing match reports and embedding them into a local ChromaDB instance!
