import streamlit as st
from resume_reader import ResumeReaderAgent
from agents import RetrieverAgent, ReasoningAgent
import os

st.set_page_config(page_title="Agentic Resume Chatbot", layout="wide")
st.title("🤖 Resume Chatbot")

# Load secrets
resume_path = "/Jugal_gurnani_Resume.pdf"
api_key = st.secrets["OPENAI_API_KEY"]

# Read resume once and cache it
@st.cache_resource
def get_resume_text(resume_path):
    reader = ResumeReaderAgent()
    return reader.read(resume_path)

resume_text = get_resume_text(resume_path)

# Initialize agents once and cache them
@st.cache_resource
def get_agents(resume_text, api_key):
    retriever = RetrieverAgent(resume_text)
    reasoner = ReasoningAgent(api_key, retriever)
    return retriever, reasoner

retriever, reasoner = get_agents(resume_text, api_key)

if "history" not in st.session_state:
    st.session_state.history = []

st.success("Resume loaded from fixed file. Start chatting below.")

user_input = st.chat_input("Interviewer/Recruiter:", key="user_input")
if user_input:
    answer = reasoner.answer(user_input, st.session_state.history)
    st.session_state.history.append({"user": user_input, "bot": answer})

# Display chat history
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat['bot'])
