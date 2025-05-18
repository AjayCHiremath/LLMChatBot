# File: ChatBot.py
import streamlit as st
from chains.chat_chain import get_chat_chain
from components.layout import build_layout
from components.input_form import get_user_input
from components.chat_display import display_chat_history
from models.ollama_model import load_llama_model
from models.parser import get_output_parser
from prompts.default_prompt import get_prompt_template
from utils.env_loader import load_environment
from utils.streaming_callback import StreamToStreamlit

# Load environment variables
load_environment(['LANGCHAIN_API_KEY', 'LANGCHAIN_TRACING_V2', 'LANGSMITH_ENDPOINT', 'LANGCHAIN_PROJECT', 'TOGETHER_API_KEY'])

# Streamlit config
st.set_page_config(layout="wide")
st.title("Streaming ChatBot using LLama 3")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "generating_response" not in st.session_state:
    st.session_state.generating_response = False

if "run_chain" not in st.session_state:
    st.session_state.run_chain = False

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Layout
response_container, input_container = build_layout()

# Display chat history first
with response_container:
    display_chat_history()

# Get user input
with input_container:
    user_input, submitted = get_user_input(disabled=st.session_state.generating_response)

# Step 1: Handle submission
if submitted and user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.generating_response = True
    st.session_state.run_chain = True
    st.session_state.current_input = user_input
    st.rerun()  # Updated to use st.rerun instead of deprecated experimental_rerun

# Step 2: Run the LLM chain
if st.session_state.run_chain:
    with response_container:
        placeholder = st.empty()
        try:
            callback = [StreamToStreamlit(placeholder)]
            prompt = get_prompt_template()
            llm = load_llama_model(callbacks=callback)
            parser = get_output_parser()
            chain = get_chat_chain(prompt=prompt, llm=llm, parser=parser)

            answer = chain.invoke({"question": st.session_state.current_input})
            st.session_state.chat_history.append(("assistant", answer))
            
        except Exception as e:
            st.error(f"Error: {e}")

        finally:
            st.session_state.generating_response = False
            st.session_state.run_chain = False
            st.session_state.current_input = ""
            st.rerun()