# Day 1: Repository Setup & Data Ingestion

Welcome to the Domain-Specific RAG System for Cricket Analytics! Here is a simple breakdown of everything we accomplished on our first day of the sprint.

## What We Did Today

1. **Set Up Our Git Repository**
   - We initialized Git to track our code changes (`git init`).
   - We created a `.gitignore` file to tell Git to ignore large data files and virtual environment folders.
   - We linked our local code to a brand new repository on GitHub and successfully pushed our code online.

2. **Created the Project Structure**
   - We set up the core folders we'll need for the project:
     - `src/`: Where all our Python code will live.
     - `data/raw/`: Where our raw, unprocessed data (like JSON files) will be stored.

3. **Isolated Our Environment**
   - We created a Python Virtual Environment (`venv`). This is like a sandbox that keeps all the libraries and dependencies for this project separate from the rest of the computer, preventing version conflicts.

4. **Wrote the Data Ingestion Script**
   - We wrote our first piece of code: `src/data_ingestion.py`.
   - This script automatically connects to [Cricsheet](https://cricsheet.org/), downloads a zip file containing historical T20 match data, and extracts all the thousands of JSON files directly into our `data/raw/` folder.
   - We ran the script and successfully populated our project with real cricket data!

## Ready for Day 2
With the repository set up and the data downloaded, we have a solid foundation. Our next step (Day 2) will be creating a local SQLite database to store and organize all this raw JSON data so we can query it efficiently!
