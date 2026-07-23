import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import our custom modules
from retriever import get_retriever
from sql_agent import get_sql_agent
from synthesizer import generate_hybrid_response

load_dotenv()

def route_query(query: str) -> str:
    """
    Routes a user query to either the 'sql' or 'vector' backend.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
    
    prompt = PromptTemplate.from_template(
        """You are an intelligent router for a Cricket Analytics system.
You must route the user's query to either 'sql', 'vector', or 'hybrid'.

Choose 'sql' if the query is strictly about specific numerical statistics, counting, or aggregations with no need for context.
Choose 'vector' if the query asks purely for historical overviews, textual reports, or prose summaries.
Choose 'hybrid' if the query asks for both specific numerical stats AND qualitative analysis or historical context (e.g., "Tell me about X's performance and their strike rate").

User Query: {query}

Respond with only exactly one word: "sql", "vector", or "hybrid".
"""
    )
    
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"query": query})
    return result.strip().lower()

def process_query(query: str) -> str:
    """
    Determines the correct backend, fetches the data, and returns the final answer.
    """
    print(f"User Query: '{query}'")
    route = route_query(query)
    print(f"--> Routing to: {route.upper()} backend")
    
    if route == 'sql':
        # Hand off to the Text-to-SQL Agent
        agent = get_sql_agent()
        response = agent.invoke({"input": query})
        output = response.get("output", "Could not fetch a response from SQL agent.")
        
        # Handle Google GenAI returning a list of content blocks instead of a raw string
        if isinstance(output, list):
            text_parts = [block.get('text', '') for block in output if isinstance(block, dict) and 'text' in block]
            if text_parts:
                return " ".join(text_parts)
            return str(output)
            
        return output
        
    elif route == 'vector':
        # Retrieve relevant text chunks
        retriever = get_retriever(k=3)
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        
        # Pass the chunks to a generative LLM for a cohesive answer
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
        rag_prompt = PromptTemplate.from_template(
            "Answer the following question based on the provided context.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )
        chain = rag_prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "query": query})
        return answer
        
    elif route == 'hybrid':
        # Route to the synthesizer for combined stats and text
        return generate_hybrid_response(query)
        
    else:
        return f"Error: Unknown routing destination '{route}'."

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables. Please set it in a .env file.")
    else:
        test_queries = [
            "Who won the T20 World Cup in 2022?",
            "How many matches are recorded in our database?",
            "Tell me about Virat Kohli's performance in recent tournaments and provide his overall batting strike rate."
        ]
        
        for q in test_queries:
            print("\n--------------------------------")
            try:
                answer = process_query(q)
                print(f"--> Final Answer:\n{answer}")
            except Exception as e:
                print(f"--> Error occurred: {e}")
