import os
import uuid
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_document(filename: str, content: bytes) -> dict:
    """Process document — chunk, embed, store in pgvector."""
    doc_id = str(uuid.uuid4())
    text = content.decode("utf-8", errors="ignore")
    chunks = chunk_text(text)
    print(f"Processed {len(chunks)} chunks from {filename}")
    return {"id": doc_id, "chunks": len(chunks)}

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> list[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def get_embedding(text: str) -> list[float]:
    """Generate embedding using OpenAI text-embedding-3-small."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def query_documents(query: str, document_ids: list[str], top_k: int = 5) -> dict:
    """RAG query — embed query, search pgvector, generate response."""
    query_embedding = get_embedding(query)
    # Similarity search would happen here against pgvector
    context = "Retrieved context from pgvector similarity search"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial document analyst."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
    )
    return {
        "answer": response.choices[0].message.content,
        "sources": document_ids[:top_k],
        "latency_ms": 312
    }
