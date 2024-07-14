import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tempfile
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
from backend.scanner import *
from backend.scrape import *
import subprocess
import json
import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = os.getenv('PINECONE_API_ENV')
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

os.environ['PINECONE_API_ENV'] = PINECONE_API_ENV
os.environ['PINECONE_API_KEY'] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)
embeddings1 = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings2 = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
INDEX_NAME_1 = "vulnerable-data"
INDEX_NAME_2 = "cve-data"
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
    # INDEX_NAME_1 = "vulnerable-data"
    # INDEX_NAME_2 = "cve-data"
    
    # embeddings1 = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # embeddings2 = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
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
                  Answer: Based on the provided context, along with general knowledge, here is a comprehensive response:
               """
    prompt = PromptTemplate.from_template(template)
    
    chain = prompt | llm
    template_data = {
        "context": context,
        "user_question": user_question
    }
    res = chain.invoke(template_data)
    return res


def fetch_cve_details(dependencies_file, output_dir):
    go_executable = "../backend/fetch.exe"
    try:
        subprocess.run([go_executable, dependencies_file, output_dir], check=True)
        # st.success("CVE details fetched successfully!")
    except subprocess.CalledProcessError as e:
        st.warning(f"Error fetching CVE details: {e}")
def create_database():
    pc.create_index(
        name=INDEX_NAME_1,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    ) 

def updatedata(result_output_file):
    loader = TextLoader(result_output_file)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    if INDEX_NAME_1 not in pc.list_indexes().names():
        create_database()
        docsearch = PineconeVectorStore.from_documents(docs, embeddings2, index_name=INDEX_NAME_1)
    else:
        docsearch = PineconeVectorStore.from_documents(docs,embedding=embeddings2,index_name = INDEX_NAME_1)

def scrape_cve_data(directory, output_file):
    try:
        scrape_cve_search_results_from_files(directory, output_file)
        # print("CVE data scraped successfully!")
    except Exception as e:
        st.warning(f"Error scraping CVE data: {e}")

def scan_notebook(uploaded_file):
    """
    Processes the uploaded .ipynb file:
        1. Extracts dependencies
        2. Checks for vulnerabilities
        3. Performs embeddings (you'll need to implement this based on your needs)
        4. Updates the database 
    """
    if uploaded_file is not None:
        try:
            # Read the content of the uploaded file
            notebook_content = uploaded_file.read().decode("utf-8")
            
            # Extract dependencies
            dependencies = extract_dependencies_from_notebook(notebook_content)
            dependencies = handle_missing_versions(dependencies)
            
            # Save dependencies to JSON
            output_file = 'dependencies.json'
            save_dependencies_to_json(dependencies, output_file)
            
            # Fetch CVE details
            dependencies_file = "dependencies.json"
            output_dir = "cve_pages"
            fetch_cve_details(dependencies_file, output_dir)
            
            # Scrape CVE data
            directory = 'cve_pages'
            result_output_file = 'results.txt'
            scrape_cve_search_results_from_files(directory, result_output_file)
            
            # Update database
            updatedata(result_output_file)
            
            st.success("Notebook scanned and database updated successfully!")
        except Exception as e:
            st.error(f"Error processing the notebook: {e}")
    else:
        st.warning("Please upload a notebook file first.")

def delete_database():
    pc.delete_index(INDEX_NAME_1)
    st.warning("Database deleted!") 