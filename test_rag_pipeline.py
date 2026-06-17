import pytest
from app.services.rag_pipeline import chunk_text, process_document

def test_chunk_text_basic():
    text = " ".join(["word"] * 1000)
    chunks = chunk_text(text, chunk_size=512, overlap=50)
    assert len(chunks) > 0
    assert all(isinstance(c, str) for c in chunks)

def test_chunk_text_overlap():
    text = " ".join([str(i) for i in range(100)])
    chunks = chunk_text(text, chunk_size=10, overlap=2)
    assert len(chunks) > 1

def test_process_document():
    content = b"Apple Inc reported revenue of $89.5 billion in Q1 2024."
    result = process_document("test.txt", content)
    assert "id" in result
    assert result["chunks"] > 0
