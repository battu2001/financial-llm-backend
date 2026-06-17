from fastapi import FastAPI
from app.api.routes import documents, query, health

app = FastAPI(
    title="Financial LLM Backend",
    description="High-traffic backend for financial document analysis using RAG and OpenAI",
    version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1/documents")
app.include_router(query.router, prefix="/api/v1")
