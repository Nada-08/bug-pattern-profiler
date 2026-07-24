# Bug Pattern Profiler

**Bug Pattern Profiler** is a cybersecurity-focused Retrieval-Augmented Generation (RAG) system that enables semantic search and AI-assisted analysis over real-world vulnerability intelligence.

Modern cybersecurity teams rely on multiple public vulnerability databases, but these sources serve different purposes and are difficult to explore using traditional keyword search. The **National Vulnerability Database (NVD)** provides comprehensive technical information about publicly disclosed vulnerabilities, including CVSS scores, CWE mappings, affected products, and attack characteristics. The **CISA Known Exploited Vulnerabilities (KEV) Catalog** is a curated list of vulnerabilities that are actively exploited in the wild, helping organizations prioritize remediation based on real-world threats.

Bug Pattern Profiler combines these complementary sources into a unified knowledge base. It ingests, normalizes, enriches, and indexes vulnerability data to enable semantic retrieval and grounded AI-generated cybersecurity analysis. Rather than functioning as a general-purpose chatbot, the system is designed to help users explore vulnerability patterns, understand security risks, and retrieve relevant threat intelligence using natural language.

## Project Goals

The project aims to:

* Aggregate vulnerability intelligence from authoritative cybersecurity sources.
* Combine NVD's technical vulnerability data with CISA KEV's exploitation intelligence into a unified retrieval corpus.
* Enable semantic search over vulnerability records instead of relying solely on keyword matching.
* Generate grounded AI-assisted vulnerability analysis using retrieved evidence.
* Provide a modular foundation for advanced retrieval techniques such as hybrid search, reranking, metadata filtering, and retrieval evaluation.

## What's Complete

### Data Ingestion Pipeline
Implemented:
- NVD CVE ingestion
- CISA KEV ingestion
- raw JSON storage
- reusable ingestion pipeline

Data sources are fetched and stored locally before normalization.

### Normalization & Enrichment
Implemented:
- unified `NormalizedDocument` schema
- cross-source schema normalization
- metadata enrichment from NVD
- KEV + NVD fusion pipeline

Current enrichment fields include:
- CVE ID
- severity
- CVSS score
- attack vector
- attack complexity
- privileges required
- exploitability score
- impact score
- CWE IDs
- vendor/product metadata
- publication dates
- exploitation metadata

### Chunking Pipeline
Implemented:
- document chunk schema
- metadata-preserving chunk generation
- chunk storage pipeline

Current chunking strategy:
- One vulnerability document = one enriched retrieval chunk

### Retrieval System
Implemented:
- SentenceTransformers embeddings
- Pinecone vector database integration
- semantic similarity retrieval
- namespace-aware retrieval
- metadata-aware retrieval support
- top-k ranked vulnerability retrieval

Embedding model:
- BAAI/bge-small-en-v1.5

Vector database:
- Pinecone serverless
- cosine similarity
- embedding dimension: 384

### RAG Generation Pipeline
Implemented:
- grounded RAG workflow
- Groq LLM integration
- structured cybersecurity prompting
- evidence-aware generation
- JSON-formatted threat intelligence outputs

Current pipeline:
```
query
→ semantic retrieval
→ context construction
→ grounded LLM generation
→ structured security analysis
```

## Current Architecture
```
NVD API + CISA KEV
        ↓
Raw JSON ingestion
        ↓
Normalization
        ↓
KEV + NVD fusion
        ↓
Chunk generation
        ↓
Embedding generation
        ↓
Pinecone vector database
        ↓
Semantic retrieval
        ↓
Grounded RAG generation
        ↓
Structured vulnerability analysis
```


## Data Sources

### National Vulnerability Database (NVD)
Source: [NVD CVE API v2.0](https://services.nvd.nist.gov/rest/json/cves/2.0)

Contains:
- CVE descriptions
- CVSS metrics
- CWE mappings
- attack metadata
- references
- vulnerability configurations

### CISA Known Exploited Vulnerabilities (KEV)
Source: [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

Contains:
- actively exploited vulnerabilities
- remediation deadlines
- exploitation metadata
- operational security prioritization data

### Data Pipeline Stages
1. **Raw**: Original API responses stored as JSON
2. **Normalized**: Unified schema with consistent field mapping
3. **Chunked**: Text broken into semantic units (~500 char chunks) with metadata

## Project Structure

```
packages/
├── common/              # Shared settings and configuration
├── ingestion/           # Data fetching and processing
│   ├── sources/         # NVD and CISA KEV fetchers
│   ├── normalize/       # Schema normalization and transformation
│   ├── chunking/        # Document chunking for search
│   ├── fusion/          # Cross-source data fusion
│   ├── storage/         # Local file I/O utilities
│   └── cli.py           # Main ingestion entry point
├── retrieval/           # Search and embedding
│   ├── embedder.py      # Text embedding service
│   ├── search_service.py # Semantic search
│   └── vector_store.py  # Pinecone integration
├── generation/          # LLM answer generation
│   ├── generation_service.py
│   └── prompts.py       # System and user prompts
├── rag/                 # End-to-end RAG orchestration
│   └── rag_service.py   # Query → Search → Generate pipeline
└── apps/                # Frontend and API applications

data/
├── raw/                 # Original API responses
│   ├── nvd/
│   └── cisa_kev/
├── normalized/          # Unified schema documents
├── chunks/              # Chunked text with metadata
└── test/                # Sample data for testing
```

## Installation

### Prerequisites
- Python 3.11+
- Pinecone account
- API Keys:
  - `GROQ_API_KEY`: For LLM generation (https://console.groq.com)
  - `PINECONE_API_KEY`: For vector search (https://www.pinecone.io)

### Setup

```bash
# Clone repository
git clone <https://github.com/Nada-08/bug-pattern-profiler>
cd bug-pattern-profiler

# Install package and dependencies
pip install -e .

# Create .env file with API keys
cat > .env << EOF
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=mixtral-8x7b-32768
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX=bug-pattern-profiler
PINECONE_ENVIRONMENT=gcp-starter
EOF
```

## Quick Start

### 1. Ingest and Process Data

```bash
# Fetch from APIs, normalize, chunk, and store locally
make ingest-local
```

### 2. Upsert to Vector Store

```bash
# Upload chunks to Pinecone for semantic search
python scripts/upsert_fused.py
```

### 3. Query with RAG

```python
from packages.rag.rag_service import RAGService

rag = RAGService()

response = rag.answer(
    query="What are the most critical CVE patterns in 2024?"
)

print(response["answer"])
print("Sources:", response["sources"])
```

## Example Capabilities
Example queries:
```
authentication bypass vulnerabilities
```

```
remote code execution vulnerabilities
```

```
privilege escalation through file handling
```

```
What are common patterns in authentication bypass vulnerabilities?
```

## Current Limitations
- Current NVD coverage is still partial and expanding
- Hybrid retrieval (BM25 + vector search) is not implemented yet
- Reranking is not implemented yet
- Evaluation harness for retrieval quality is still under development
- Some enrichment fields may be missing when matching NVD entries are unavailable
- Current chunking strategy is intentionally simple

## Roadmap & Next Steps

### Phase 2: Retrieval Improvements
Planned:
- retrieval evaluation framework
- hybrid retrieval (BM25 + dense retrieval)
- reranking layer
- improved chunking strategies
- metadata filtering improvements

### Phase 3: APIs & Applications
Planned:
- FastAPI backend
- frontend dashboard
- deployment pipeline
- AWS infrastructure

### Technology Stack
### Core
- Python
- HTTPX

### AI / Retrieval
- SentenceTransformers
- Pinecone
- Groq LLM
- RAG architecture

### Models
Embedding:
```
BAAI/bge-small-en-v1.5
```

Generation: 
```
Llama-3.3-70b-versatile
```
---
**Status**: Active Development · **Last Updated**: 2026-05-07
