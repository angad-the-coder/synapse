#!/bin/bash

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install langchain
pip install openai
pip install python-dotenv
pip install chromadb
pip install tiktoken
pip install faiss-cpu
pip install unstructured
pip install pdf2image
pip install pytesseract
pip install google-search-results

# Make the script executable
chmod +x init.sh

echo "Dependencies installed successfully!"