# Financial LLM Backend — Intelligent Document Analysis Platform

A high-traffic, production-grade backend service for automated financial document analysis using LLM-powered pipelines, Retrieval-Augmented Generation (RAG), and vector search. Built with Python, FastAPI, Django, OpenAI API, PostgreSQL (pgvector), Redis, Docker, and AWS Lambda.

---

## Overview

This system processes large volumes of financial documents (earnings reports, SEC filings, analyst reports) and enables real-time intelligent querying using a RAG pipeline. It reduces manual document review time by 40% and supports high-concurrency access via Redis caching and serverless AWS Lambda functions.

---

## Architecture

```
Client Request
      │
      ▼
 FastAPI Gateway
      │
      ├──► Django ORM ──► PostgreSQL (pgvector)
      │         │               │
      │         │         Vector Embeddings
      │         │         (OpenAI Embeddings API)
      │         ▼
      │      Redis Cache
      │      (low-latency retrieval)
      │
      ├──► RAG Pipeline
      │         │
      │         ├── Document Chunking
      │         ├── Embedding Generation
      │         ├── pgvector Similarity Search
      │         └── OpenAI GPT Response Generation
      │
      └──► AWS Lambda (serverless batch ingestion)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI, Django |
| LLM Integration | OpenAI API (GPT-4, Embeddings) |
| Vector Store | PostgreSQL + pgvector |
| Caching | Redis |
| Serverless Ingestion | AWS Lambda |
| Containerization | Docker |
| Cloud | AWS (EC2, S3, RDS, Lambda, CloudWatch) |
| Testing | pytest (unit + integration) |
| Language | Python 3.11 |

---

## Features

- **RAG Pipeline** — chunks documents, generates embeddings via OpenAI, stores in pgvector, and retrieves domain-specific context for real-time query responses
- **High-traffic API** — FastAPI gateway handles concurrent requests with Redis caching reducing DB hits by 60%
- **Serverless ingestion** — AWS Lambda functions batch-process new document uploads from S3
- **Unit & integration tests** — pytest test suite covering API endpoints, RAG pipeline stages, and database operations
- **Production monitoring** — AWS CloudWatch metrics and alerts for latency, error rates, and throughput
- **Full ownership** — designed, built, and deployed end-to-end from schema design through production monitoring

---

## Project Structure

```
financial-llm-backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── documents.py       # Document upload & management endpoints
│   │   │   ├── query.py           # RAG query endpoints
│   │   │   └── health.py          # Health check endpoints
│   │   └── dependencies.py        # Auth, DB session, Redis client
│   ├── core/
│   │   ├── config.py              # Environment config (AWS, OpenAI, DB)
│   │   └── security.py            # API key auth
│   ├── models/
│   │   ├── document.py            # Django ORM models
│   │   └── embedding.py           # pgvector embedding model
│   ├── services/
│   │   ├── rag_pipeline.py        # RAG orchestration
│   │   ├── embeddings.py          # OpenAI embedding generation
│   │   ├── vector_search.py       # pgvector similarity search
│   │   └── cache.py               # Redis caching layer
│   └── lambda/
│       └── ingest_handler.py      # AWS Lambda document ingestion
├── tests/
│   ├── unit/
│   │   ├── test_rag_pipeline.py
│   │   ├── test_embeddings.py
│   │   └── test_vector_search.py
│   └── integration/
│       ├── test_api_endpoints.py
│       └── test_pipeline_e2e.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ with pgvector extension
- Redis 7+
- AWS account (for Lambda + S3)
- OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/battu2001/financial-llm-backend.git
cd financial-llm-backend
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/financial_llm
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
```

### 3. Start services with Docker Compose

```bash
docker-compose up -d
```

This starts PostgreSQL (with pgvector), Redis, and the FastAPI application.

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. Enable pgvector extension

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 6. Run tests

```bash
pytest tests/ -v
```

### 7. Start the API server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/documents/upload` | Upload a financial document |
| GET | `/api/v1/documents/{id}` | Retrieve document metadata |
| POST | `/api/v1/query` | RAG-powered document query |
| GET | `/api/v1/health` | Health check |

### Example — Query a document

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was the revenue growth in Q3?",
    "document_ids": ["doc_123", "doc_456"],
    "top_k": 5
  }'
```

**Response:**

```json
{
  "answer": "Revenue grew 18% year-over-year in Q3, driven by...",
  "sources": [
    { "document_id": "doc_123", "chunk": "...", "similarity_score": 0.94 }
  ],
  "latency_ms": 312
}
```

---

## RAG Pipeline — How It Works

1. **Document ingestion** — PDF/text uploaded via API or S3 trigger (Lambda)
2. **Chunking** — document split into overlapping chunks (512 tokens, 50 token overlap)
3. **Embedding** — each chunk embedded via `text-embedding-3-small` (OpenAI)
4. **Storage** — embeddings stored in PostgreSQL using pgvector `vector(1536)` column
5. **Query** — user query embedded → cosine similarity search against pgvector → top-K chunks retrieved
6. **Generation** — retrieved chunks + query sent to GPT-4 → response returned

---

## Performance

| Metric | Value |
|---|---|
| API response latency (p95) | < 400ms |
| Cache hit rate (Redis) | ~65% |
| Manual review time reduction | 40% |
| Test coverage | 85%+ |

---

## Key Engineering Decisions

- **pgvector over Pinecone** — keeps vector search co-located with relational data, reducing network hops and operational complexity
- **Redis caching** — frequent queries cached with TTL to reduce OpenAI API costs and DB load
- **Serverless ingestion** — AWS Lambda handles bursty document uploads without over-provisioning EC2
- **Async FastAPI** — async endpoints + connection pooling handle high-concurrency workloads efficiently

---

## License

MIT

