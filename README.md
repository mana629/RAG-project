# Local RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) system powered by **Google Gemini** and **LangChain**.

## Features

- **Google Generative AI Embeddings**: High-dimensional vector embeddings with `models/text-embedding-004`.
- **Vector Store**: Fast CPU-based similarity search using **FAISS**.
- **Multi-format Document Ingestion**: Support for PDF, DOCX, and text documents.
- **Interactive UI**: Clean interface built with **Streamlit**.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mana629/RAG-project.git
   cd RAG-project
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Windows (Command Prompt):
   venv\Scripts\activate.bat
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and insert your Google API key:
   ```dotenv
   GOOGLE_API_KEY=your_actual_google_api_key
   GOOGLE_CHAT_MODEL=gemini-1.5-flash
   EMBEDDING_MODEL=models/text-embedding-004
   TOP_K=4
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=150
   ```
