import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import our custom modules
from retriever import get_retriever
from sql_agent import get_sql_agent

load_dotenv()

def route_query(query: str) -> str:
    """
    Routes a user query to either the 'sql' or 'vector' backend.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = PromptTemplate.from_template(
        """You are an intelligent router for a Cricket Analytics system.
You must route the user's query to either the 'sql' database or the 'vector' database.

Choose 'sql' if the query is about specific statistics, match outcomes, player details, ball-by-ball analysis, or requires counting and aggregations.
Choose 'vector' if the query asks for summaries, historical overviews, textual reports, or general prose descriptions of matches or tournaments.

User Query: {query}

Respond with only exactly one word: either "sql" or "vector".
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
        return response.get("output", "Could not fetch a response from SQL agent.")
        
    elif route == 'vector':
        # Retrieve relevant text chunks
        retriever = get_retriever(k=3)
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        
        # Pass the chunks to a generative LLM for a cohesive answer
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        rag_prompt = PromptTemplate.from_template(
            "Answer the following question based on the provided context.\n\nContext:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        )
        chain = rag_prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "query": query})
        return answer
        
    else:
        return f"Error: Unknown routing destination '{route}'."

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables. Please set it in a .env file.")
    else:
        test_queries = [
            "Who won the T20 World Cup in 2022?",
            "How many matches are recorded in our database?"
        ]
        
        for q in test_queries:
            print("\n--------------------------------")
            try:
                answer = process_query(q)
                print(f"--> Final Answer:\n{answer}")
            except Exception as e:
                print(f"--> Error occurred: {e}")
