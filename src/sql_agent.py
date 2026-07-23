import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "cricket.db")

def get_sql_agent():
    """Initializes and returns a LangChain SQL Agent connected to our SQLite DB."""
    # Initialize the database connection
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    
    # Initialize the LLM
    # Note: Requires OPENAI_API_KEY in the environment or a .env file
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
    
    # Create the SQL agent
    agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling", verbose=True)
    return agent_executor

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment variables. Please set it in a .env file to run the test.")
    else:
        print("Initializing SQL Agent...")
        agent = get_sql_agent()
        query = "How many matches did India win?"
        print(f"\nTesting SQL Agent with query: '{query}'\n")
        try:
            response = agent.invoke({"input": query})
            print("\n--- Agent Response ---")
            print(response["output"])
        except Exception as e:
            print("\nError executing SQL Agent:", e)
