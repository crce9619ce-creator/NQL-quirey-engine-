from fastapi import APIRouter, HTTPException
from ..services.schema_discovery import SchemaDiscovery
import os

router = APIRouter()

@router.get('/')
def get_schema():
    db = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'demo.db')
    sd = SchemaDiscovery(db)
    return sd.analyze_database()
