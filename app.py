import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Add the 'src' directory to the Python path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from query_router import process_query, route_query

# Setup Streamlit page configuration
st.set_page_config(
    page_title="Cricket Analytics RAG",
    page_icon="🏏",
    layout="centered"
)

st.title("🏏 Cricket Analytics RAG System")
st.markdown("Ask anything about cricket matches, players, statistics, and tournament history!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., What is Virat Kohli's batting strike rate?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if GOOGLE_API_KEY is present
    if not os.environ.get("GOOGLE_API_KEY"):
        with st.chat_message("assistant"):
            st.error("⚠️ GOOGLE_API_KEY is missing. Please set it in your `.env` file or environment variables.")
        st.stop()

    with st.spinner("Analyzing query and fetching data..."):
        try:
            # Determine routing just for UI display (optional, but requested in plan)
            route = route_query(prompt)
            st.info(f"🔍 **Routed via**: `{route.upper()}` backend")
            
            # Process the actual query
            response = process_query(prompt)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
                
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"An error occurred: {e}")
