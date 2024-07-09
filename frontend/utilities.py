from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

os.environ['PINECONE_API_ENV'] = PINECONE_API_ENV
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Pinecone
pinecone = Pinecone(api_key=PINECONE_API_KEY)


def query_pinecone(index_name, query, embeddings):
    try:
        docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
        result = docsearch.similarity_search(query)
        return result
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return []

def get_context_from_pinecone(query):
    INDEX_NAME_1 = "cve-data-googlembeddings"
    INDEX_NAME_2 = "cve-data"
    
    embeddings1 = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings2 = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    results_1 = query_pinecone(INDEX_NAME_1, query, embeddings2)
    results_2 = query_pinecone(INDEX_NAME_2, query, embeddings1)

    context = ""
    for match in results_1 + results_2:
        context += match.page_content
    return context

def get_chatbot_response(user_question):
    llm = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))
    context = get_context_from_pinecone(user_question)
    
    template = """Context: {context}
                  Question: {user_question}
                  Answer: Let's think step by step.
               """
    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | llm
    template_data = {
        "context": context,
        "user_question": user_question
    }
    res = chain.invoke(template_data)
    return res


def scan_notebook(uploaded_file):
    """
    Processes the uploaded .ipynb file:
        1. Extracts dependencies
        2. Checks for vulnerabilities
        3. Performs embeddings (you'll need to implement this based on your needs)
        4. Updates the database 
    """
    if uploaded_file is not None:
        # 1. Process the uploaded file
        try:
            notebook_content = uploaded_file.read().decode("utf-8")
            # ... (Your logic to extract dependencies, check vulnerabilities, etc.)
            st.success("Notebook scanned and database updated successfully!")
        except Exception as e:
            st.error(f"Error processing the notebook: {e}")

def delete_database():
    """Deletes the database (implementation depends on your database setup)"""
    # ... (Add your database deletion logic here)
    st.warning("Database deleted!") 