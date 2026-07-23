import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import custom modules
from ner import extract_cricket_entities
from metrics import calculate_custom_metrics
from retriever import get_retriever

load_dotenv()

def generate_hybrid_response(query: str) -> str:
    """
    Synthesizes a response by combining statistical data (via NER and Metrics) 
    and unstructured textual data (via vector DB).
    """
    print(f"--- Synthesizing Response for: '{query}' ---")
    
    # 1. Extract Entities
    print("1. Extracting Entities...")
    entities = extract_cricket_entities(query)
    
    # 2. Calculate Stats
    print("2. Calculating Custom Metrics...")
    stats_data = calculate_custom_metrics(entities)
    stats_json = json.dumps(stats_data, indent=2)
    
    # 3. Retrieve Unstructured Text
    print("3. Retrieving Contextual Text...")
    retriever = get_retriever(k=3)
    docs = retriever.invoke(query)
    retrieved_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 4. Synthesize with Generative LLM
    print("4. Generating Final Response...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    system_prompt = """You are an expert Cricket Analyst. Your job is to answer the user's question by combining exact statistical metrics with historical textual context.

You are provided with two sources of information:
1. 'Statistical Data': Exact metrics (runs, wickets, strike rates, averages) calculated from our ball-by-ball database for the entities mentioned in the query.
2. 'Textual Context': Relevant paragraphs retrieved from match reports and articles.

Instructions:
- Seamlessly weave the exact statistical figures into your narrative.
- Use the Textual Context to provide qualitative background (e.g., how the player performed in a specific tournament, context around their stats).
- If the Statistical Data contains the answer (like Strike Rate), use those exact numbers. Do not make up numbers.
- If no stats or context are relevant, simply answer based on your knowledge, but prioritize the provided data.

---
Statistical Data:
{stats}

---
Textual Context:
{context}

---
User Question: {query}
"""

    prompt = PromptTemplate.from_template(system_prompt)
    chain = prompt | llm | StrOutputParser()
    
    final_answer = chain.invoke({
        "stats": stats_json,
        "context": retrieved_text,
        "query": query
    })
    
    return final_answer

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found. Please set it in .env")
    else:
        test_query = "Tell me about Virat Kohli's performance, including his overall batting strike rate."
        answer = generate_hybrid_response(test_query)
        print("\n=== Final Output ===")
        print(answer)
