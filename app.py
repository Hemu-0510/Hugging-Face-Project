import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Page settings
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Check token
if not HF_TOKEN:
    st.error("❌ Hugging Face token not found.")
    st.stop()

# Hugging Face OpenAI-compatible client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# Title
st.title("🤖 AI Chat Assistant")

st.write(
    "Ask questions about studies, coding, mathematics, "
    "career, writing, technology and general topics."
)

# Sidebar
with st.sidebar:

    st.header("✨ What can I help with?")

    st.write("📚 Study & Learning")
    st.write("💻 Programming & Coding")
    st.write("➗ Mathematics")
    st.write("📝 Writing & Grammar")
    st.write("🎯 Career Guidance")
    st.write("💡 Project Ideas")
    st.write("🌍 General Knowledge")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_message = st.chat_input("💬 Ask anything...")

if user_message:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            try:

                response = client.chat.completions.create(

                    model="meta-llama/Llama-3.1-8B-Instruct:novita",

                    messages=[
                        {
                            "role": "system",
                            "content": """
You are a helpful general-purpose AI assistant.

Help users with:
- Education
- Programming
- Mathematics
- Science
- Writing
- Career guidance
- Interview preparation
- Technology
- Project ideas
- General knowledge
- Everyday questions

Give clear, simple and useful answers.
For students, explain difficult concepts step by step.
For coding questions, provide beginner-friendly examples.
"""
                        },
                        *st.session_state.messages
                    ],

                    max_tokens=600,
                    temperature=0.7
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save AI answer
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error("❌ Unable to get a response.")

                st.code(str(e))