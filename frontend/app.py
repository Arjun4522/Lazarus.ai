import streamlit as st
from utilities import *
try:
    with open("dependencies.json", "r") as f:
        dependencies = json.load(f)
except:
    st.warning("Please Scan The Notebook To View Dependencies")

st.title("Security Assistance Chatbot")
st.sidebar.title("Actions")
uploaded_file = st.sidebar.file_uploader("Upload .ipynb file", type=["ipynb"])
st.sidebar.button("Scan", on_click=scan_notebook, args=(uploaded_file,))
st.sidebar.button("Delete Database", on_click=delete_database) 
try:
    show_dependencies(dependencies=dependencies)
except:
    ""
# try:
#     st.sidebar.button("Show dependencies", on_click=show_dependencies(dependencies))
# except:
#     st.write("")
    
# st.sidebar.button("Close", on_click=close_dependencies)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "dependencies_displayed" not in st.session_state:
    st.session_state.dependencies_displayed = False

if st.session_state.dependencies_displayed:
    with st.sidebar.expander("Dependencies"):
        for dependency, version in dependencies.items():
            st.write(f"{dependency}: {version}")

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

