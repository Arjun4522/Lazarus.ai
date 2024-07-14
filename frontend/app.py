import streamlit as st
from utilities import *



st.set_page_config(page_title="Security Assistance Chatbot")
st.title("Security Assistance Chatbot")
st.sidebar.title("Actions")
uploaded_file = st.sidebar.file_uploader("Upload .ipynb file", type=["ipynb"])
st.sidebar.button("Scan", on_click=scan_notebook, args=(uploaded_file,))
st.sidebar.button("Delete Database", on_click=delete_database) 

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("You:")

if user_input:
   
    st.session_state.messages.append({"role": "user", "content": user_input})

   
    with st.chat_message("user"):
        st.markdown(user_input)

  
    with st.spinner("Thinking..."):
        response = get_chatbot_response(user_input) 
        st.session_state.messages.append({"role": "assistant", "content": response})

    
        with st.chat_message("assistant"):
            st.markdown(response)

