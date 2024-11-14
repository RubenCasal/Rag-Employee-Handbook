import streamlit as st
from agent import Agent
st.title("Rag Employee Handbook")


agent = Agent()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])
prompt = st.chat_input("Pass your prompt here")

if prompt:
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    response = agent.answer_user(query=prompt)
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role':'assistant','content':response})