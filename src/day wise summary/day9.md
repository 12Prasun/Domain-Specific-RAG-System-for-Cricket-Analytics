# Day 9: Statistical Reasoning Logic

Welcome to Day 9 of the Domain-Specific RAG System for Cricket Analytics sprint. Building upon the entity extraction implemented on Day 8, today we added a robust statistical reasoning module to calculate custom cricket metrics.

## What We Accomplished Today

1. **Custom Metrics Module (`src/metrics.py`)**
   - We created a new standalone Python module, `metrics.py`, to directly interface with our SQLite `cricket.db` database.
   - We established specific SQL queries to calculate custom metrics using ball-by-ball and match-level data.

2. **Player Level Statistics**
   - **Batting Stats**: Implemented logic to calculate a player's `Runs Scored`, `Balls Faced`, `Times Dismissed`, `Batting Average`, and `Strike Rate`.
   - **Bowling Stats**: Implemented logic to calculate a player's `Runs Conceded`, `Balls Bowled` (converted to Overs), `Wickets Taken` (excluding non-bowler specific dismissals like run outs), `Economy Rate`, and `Bowling Average`.

3. **Team Level Statistics**
   - Implemented logic to calculate an entity team's total `Matches Played`, `Matches Won`, and overall `Win Percentage`.

4. **Integration with NER**
   - Created the `calculate_custom_metrics(entities: dict)` function, designed specifically to intake the categorized entities (players and teams) extracted by our `ner.py` script.
   - Tested the system with well-known players (e.g., Virat Kohli, Jasprit Bumrah) and confirmed that accurate statistical calculations are generated dynamically based on the dataset.

## Verification
We ran tests against the `cricket.db` for several players and successfully returned structured JSON containing their historical stats, seamlessly integrating our previously structured data with newly implemented reasoning logic.

## Next Steps
In Day 10, we'll focus on prompt engineering to synthesize the information from the RAG retriever (from Day 4-5) and our custom statistical reasoning logic into natural language answers for the user!
