# Use a suitable base image for Streamlit
FROM python:3.10.14-bookworm

# Set environment variables for Streamlit (if needed)
ENV STREAMLIT_SERVER_PORT=8501 

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit app when container starts
CMD ["streamlit", "run", "app.py"]  