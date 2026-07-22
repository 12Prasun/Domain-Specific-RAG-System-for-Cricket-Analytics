# Day 8: Sports-Specific NER

## What was implemented today
We implemented a robust Named Entity Recognition (NER) module customized for the cricket domain. This module is responsible for extracting specific cricket entities (players, teams, bowling styles, shots, etc.) from unstructured natural language text.

### Key Changes
- **`src/ner.py`**: Created a new standalone module for entity extraction.
- **Pydantic Schema `CricketEntities`**: Defined a typed schema to guide the LLM using LangChain's structured output. This ensures that the model reliably outputs lists of strings for predefined categories.
- **Custom Classification Logic (`BOWLING_CLASSIFICATION`)**: Introduced a domain-specific dictionary mapping colloquial terms (like "googly", "doosra", "yorker") to broader bowling classifications ("Spin Bowling", "Pace Bowling").
- **Integration Function**: Added `extract_cricket_entities(text)` which strings together the LangChain prompt, the LLM with structured output, and our custom python logic to deliver a clean dictionary of extracted entities.

## Testing & Verification
The `ner.py` file includes a `__main__` block with synthetic test queries:
1. *"How many wickets did Rashid Khan take with his googly in the IPL 2023?"*
2. *"Show me MS Dhoni's helicopter shots against Pakistan."*
3. *"Did Jasprit Bumrah bowl a yorker to get Steve Smith out in the Border Gavaskar Trophy?"*

> [!NOTE]
> When executing `python src/ner.py`, ensure that your `OPENAI_API_KEY` is properly set in your `.env` file, as the module relies on `gpt-3.5-turbo` for extraction.

## Next Steps
In Day 9, we will implement statistical reasoning logic to calculate complex custom metrics, utilizing the entities we've begun to structure here.
