# NLP Query Engine - Reorganized Project

This repository is a reorganized skeleton of the NLP Query Engine with FAISS vector store and PDF/DOCX parsing.

Structure:
- backend/api/services - core services (schema discovery, document processing, query engine, vector store)
- backend/api/routes - FastAPI route modules for ingestion, schema, and query
- frontend/src - React components (simple UI)
- requirements.txt - Python deps
- package.json - frontend deps and scripts

Quick start (backend):
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

Notes:
- `sentence-transformers` model will be downloaded at first run.
- FAISS may be platform-specific; if `faiss-cpu` fails to install, consider `hnswlib` or a hosted vector DB.
