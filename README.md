# Local RAG Knowledge Assistant

A robust, production-ready **Retrieval-Augmented Generation (RAG)** pipeline designed for enterprise knowledge extraction, document search, and conversational Q&A powered by **Google Gemini** and **LangChain**.

---

## 📌 Architecture Overview

```
[ Documents (.pdf, .docx) ]
             │
             ▼
[ Document Loader (`src/loader.py`) ] ───► Normalizes Metadata & Cleans Content
             │
             ▼
[ Text Splitter (Recursive Splitting) ] ──► Chunk Size: 1000 | Overlap: 150
             │
             ▼
[ Embedding Engine (`src/embedding.py`) ] ─► Google Gemini `models/text-embedding-004`
             │
             ▼
[ Vector Store (FAISS) ] ──────────────► CPU-based Indexed Similarity Search
             │
             ▼
[ Retrieval & Generation (Gemini 1.5) ] ─► Grounded, Context-Aware Answers
```

---

## ✨ Features

- **Multi-Format Document Ingestion**: Seamless parsing of `.pdf` and `.docx` files via `PyPDFLoader` and `Docx2txtLoader`.
- **Intelligent Metadata Enrichment**: Automatically attaches cleaned file names, page numbers, and sources to prevent hallucination during retrieval.
- **Configurable Text Chunking**: Recursive character splitting with fine-tuned overlap parameters for optimal contextual continuity.
- **State-of-the-Art Google Embeddings**: Powered by Google Generative AI's `models/text-embedding-004`.
- **Lightweight CPU Vector Search**: Integrated with **FAISS CPU** for ultra-fast local index storage and retrieval without requiring heavy GPU drivers.
- **Streamlit Interactive Frontend**: Clean, responsive user interface for uploading files and querying your documents.

---

## 📂 Project Structure

```
RAG-project/
├── src/
│   ├── __init__.py           # Package marker
│   ├── loader.py             # Document ingestion, sanitization & chunking
│   └── embedding.py          # Google Gemini embedding engine
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore configuration (protects .env & venv)
├── README.md                 # Complete project documentation
├── requirements.txt          # Python dependencies
└── venv/                     # Local virtual environment
```

---

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mana629/RAG-project.git
cd RAG-project
```

### 2. Create & Activate Virtual Environment
* **PowerShell (Windows):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
* **Command Prompt (Windows):**
  ```cmd
  venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```
Update your `.env` with your Google AI Studio credentials:
```dotenv
GOOGLE_API_KEY=your_actual_google_api_key
GOOGLE_CHAT_MODEL=gemini-1.5-flash
EMBEDDING_MODEL=models/text-embedding-004
TOP_K=4
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
```

> **Note**: Obtain a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🛠️ Usage & Module Reference

### 1. Document Loading (`src/loader.py`)
Load and split documents from any local folder:
```python
from src.loader import load_documents, split_documents

# Load all PDF and DOCX files from a directory
docs = load_documents("./data_folder")
print(f"Loaded {len(docs)} document pages.")

# Split documents into chunks for embedding
chunks = split_documents(docs, chunk_size=1000, chunk_overlap=150)
print(f"Created {len(chunks)} text chunks.")
```

### 2. Embeddings Engine (`src/embedding.py`)
Initialize and generate embeddings using Google Gemini:
```python
from src.embedding import get_embedding_model, get_embedding_model_name

# Retrieve the initialized model
model = get_embedding_model()
print(f"Active model: {get_embedding_model_name()}")

# Generate vector embeddings
vector = model.embed_query("Explain retrieval-augmented generation.")
print(f"Embedding dimension: {len(vector)}")
```

---

## 🔒 Security & Privacy

- Sensitive credentials like `GOOGLE_API_KEY` are stored strictly in `.env` and are strictly excluded from version control via `.gitignore`.
- All document processing occurs locally, passing chunks only to Google's embedding and generative APIs during vector indexing and query resolution.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
