# Lazarus.ai

An advanced MLSecOps platform designed for seamless integration with any ML model deployment workflow. It meticulously scans for potential bugs and security vulnerabilities at every stage of the CI/CD pipeline. Equipped with an intuitive in-built chat UI, Lazarus.ai enhances the vulnerability management process, ensuring it is both comprehensive and reliable.

## Features

- **Chat Interface:** Interact with the chatbot using a user-friendly chat interface.
- **CVE Information Retrieval:** Ask questions about specific CVEs, and the chatbot will try to provide relevant information. 
- **Dependency Scanning :** Upload Jupyter Notebook (.ipynb) files to extract dependencies and check for known vulnerabilities.
- **Code Scanning (work in progress):** Static analysis to check for code vulnerabilities.
- **Container Scanning (work in progress):** Scanning containers, docker images and K8 clusters to check for code vulnerabilities.
- **Vector Database Integration :** Stores CVE information and potentially scan results in a database for efficient retrieval.

## Prerequisites

- **Python 3.10 or higher:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **pip (Python package installer):** Usually installed with Python.

## Installation

**Clone the repository:**
   
   `git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name`

Create a virtual environment (recommended):
   
   `python -m venv .venv
   source .venv/bin/activate`
   
 ### On Windows:
 
    `.venv\Scripts\activate`

Install the required packages:

   `pip install -r requirements.txt`

### Optional] Set Up Your Database (if used):

Follow the instructions in the database setup documentation (if provided) to create and configure your database.
[Optional] Set Up API Keys and Environment Variables (if used):

Create a .env file in the root directory.
Add your API keys and other sensitive information as environment variables in the .env file (see the .env.example file for a template).
Running the Application

Activate the virtual environment (if you created one):

   `source .venv/bin/activate`

## Run

Run the Streamlit app:

   `streamlit run app.py`

This will start the Streamlit development server, and the chatbot interface will open in your web browser.
Usage
Type your questions or requests into the chat input field at the bottom of the interface.
[Optional] Use the sidebar (if implemented) to upload .ipynb files for dependency scanning or to manage the database.

Contributing

Fork the repository.
Create a new branch for your feature (git checkout -b feature/your-feature-name).
Make your changes and commit them (git commit -am 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Open a pull request.
