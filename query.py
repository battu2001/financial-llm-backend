from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_pipeline import query_documents

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    document_ids: list[str]
    top_k: int = 5

@router.post("/query")
def query_document(request: QueryRequest):
    result = query_documents(request.query, request.document_ids, request.top_k)
    return result
