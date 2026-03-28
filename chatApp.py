import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

from auth import init_auth, show_auth_page, logout

load_dotenv()

@st.cache_resource
def get_client():
    from openai import OpenAI
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = get_client()



init_auth()

if not st.session_state.authenticated:
    show_auth_page()


st.set_page_config(page_title="AI Chat App", page_icon="💬")

st.title("💬 AI Chat Application")

st.sidebar.write(f"👋 {st.session_state.username}")

if st.sidebar.button("Logout"):
    logout()



if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                response_container.markdown(full_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })