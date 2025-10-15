from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.schema_discovery import SchemaDiscovery
from ..services.document_processor import DocumentProcessor
from ..services.query_engine import QueryEngine
from ..services.vector_store import VectorStore
import os

router = APIRouter()

class QueryRequest(BaseModel):
    q: str

# For demo we re-instantiate services here; main.py can wire real singletons
@router.post('/')
def run_query(req: QueryRequest):
    base = os.path.join(os.path.dirname(__file__), '..', '..')
    db = os.path.join(base, 'data', 'demo.db')
    vector_dir = os.path.join(base, 'vector_data')
    os.makedirs(vector_dir, exist_ok=True)
    sd = SchemaDiscovery(db)
    vs = VectorStore(vector_dir)
    dp = DocumentProcessor(os.path.join(base, 'documents'), vector_store=vs)
    qe = QueryEngine(db, sd, dp)
    return qe.process_query(req.q)
