import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

class CricketEntities(BaseModel):
    """Identifying cricket-specific entities in a text."""
    players: List[str] = Field(default_factory=list, description="Names of cricket players")
    teams: List[str] = Field(default_factory=list, description="Names of cricket teams or countries")
    bowling_styles: List[str] = Field(default_factory=list, description="Types of bowling deliveries or styles mentioned (e.g., googly, yorker, spin)")
    shot_types: List[str] = Field(default_factory=list, description="Types of batting shots mentioned (e.g., cover drive, helicopter shot)")
    tournaments: List[str] = Field(default_factory=list, description="Names of cricket tournaments or series")

# Dictionary for mapping specific colloquialisms to broader classifications
BOWLING_CLASSIFICATION = {
    "googly": "Spin Bowling",
    "doosra": "Spin Bowling",
    "leg-break": "Spin Bowling",
    "off-break": "Spin Bowling",
    "carrom ball": "Spin Bowling",
    "flipper": "Spin Bowling",
    "slider": "Spin Bowling",
    "bouncer": "Pace Bowling",
    "yorker": "Pace Bowling",
    "slower ball": "Pace Bowling",
    "in-swing": "Pace Bowling",
    "out-swing": "Pace Bowling",
    "reverse swing": "Pace Bowling",
    "cutter": "Pace Bowling"
}

def classify_entities(entities: CricketEntities) -> dict:
    """Applies custom domain logic to classify extracted entities into broader categories."""
    result = entities.model_dump()
    
    # Classify bowling styles
    classified_bowling = []
    for style in result.get("bowling_styles", []):
        style_lower = style.lower()
        classification = None
        for key, category in BOWLING_CLASSIFICATION.items():
            if key in style_lower:
                classification = category
                break
        
        if classification and classification not in classified_bowling:
            classified_bowling.append(classification)
        elif not classification and style not in classified_bowling:
            classified_bowling.append(style)
            
    result["classified_bowling_styles"] = classified_bowling
    return result

def extract_cricket_entities(text: str) -> dict:
    """Extracts and classifies cricket entities from the given text."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    structured_llm = llm.with_structured_output(CricketEntities)
    
    prompt = PromptTemplate.from_template(
        "Extract the relevant cricket entities from the following text:\n\n{text}"
    )
    
    chain = prompt | structured_llm
    
    # Invoke the chain
    extracted_entities: CricketEntities = chain.invoke({"text": text})
    
    # Apply custom classification
    return classify_entities(extracted_entities)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")
    else:
        test_queries = [
            "How many wickets did Rashid Khan take with his googly in the IPL 2023?",
            "Show me MS Dhoni's helicopter shots against Pakistan.",
            "Did Jasprit Bumrah bowl a yorker to get Steve Smith out in the Border Gavaskar Trophy?"
        ]
        
        for q in test_queries:
            print(f"\nText: {q}")
            try:
                entities = extract_cricket_entities(q)
                print(f"Extracted Entities: {entities}")
            except Exception as e:
                print(f"Error occurred: {e}")
