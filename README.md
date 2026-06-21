# Enterprise RAG Assistant

A secure document question-answering assistant built with FastAPI, LangGraph, Qdrant, and Streamlit.

## Features

- PDF upload
- Text extraction
- Chunking
- Vector search with Qdrant
- RAG answer generation
- Citations
- API key authentication
- Prompt-injection guardrails
- Streamlit chat interface
- Document management

## Tech Stack

- Python
- FastAPI
- LangGraph
- Qdrant
- Sentence Transformers
- OpenAI API
- Streamlit

## Project Structure

```text
backend/
  app/
    main.py
    pdf_loader.py
    chunker.py
    vector_store.py
    rag_pipeline.py
    rag_graph.py
    security.py
    guardrails.py
frontend/
  streamlit_app.py

## Project Setup 
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

OPENAI_API_KEY=your_key_here
APP_API_KEY=your_secret_key


## Run Backend
uvicorn backend.app.main:app
## Run FrontEnd
streamlit run frontend/streamlit_app.py

## API Endpoints
POST /upload-pdf
GET /ask
GET /search
GET /documents
DELETE /documents

## Security Features
API key authentication
Basic prompt-injection detection
Context-grounded answers
Source citations
