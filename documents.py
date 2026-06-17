from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag_pipeline import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files supported")
    content = await file.read()
    result = process_document(file.filename, content)
    return {"message": "Document processed successfully", "document_id": result["id"]}

@router.get("/{document_id}")
def get_document(document_id: str):
    return {"document_id": document_id, "status": "processed"}
