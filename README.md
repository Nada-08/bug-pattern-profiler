# Bug Pattern Profiler

Bug Pattern Profiler is a cybersecurity Retrieval-Augmented Generation (RAG) project for exploring vulnerability intelligence from the National Vulnerability Database (NVD) and CISA's Known Exploited Vulnerabilities (KEV) catalog.

It builds NVD, KEV, and fused KEV+NVD document collections, indexes their enriched vulnerability metadata in Pinecone, retrieves and reranks relevant CVEs from natural-language queries, and can generate a grounded analysis with Groq or expose it through a FastAPI service.

## Implemented

- Fetch, normalize, and store NVD CVE and CISA KEV records locally.
- Fuse KEV exploitation information with matching NVD technical metadata.
- Create metadata-preserving retrieval chunks (currently one enriched chunk per vulnerability document).
- Embed chunks with `BAAI/bge-small-en-v1.5` and upsert them to Pinecone namespaces.
- Run dense semantic search, cross-encoder reranking with `BAAI/bge-reranker-v2-m3`, and map matches to structured `SearchResult` objects.
- Merge NVD and fused retrieval candidates by CVE, preserve the richer metadata, rerank the combined set, and use it for RAG answers.
- Normalize common CVE/CWE query formats and extract CVE IDs, CWE IDs, and publication dates.
- Apply Pinecone metadata filters for explicitly requested CVE or CWE identifiers.
- Resolve likely vendor and product mentions against a locally built corpus vocabulary; the resolved values are captured for query analysis, while vendor/product filtering is not enabled yet.
- Generate grounded, JSON-shaped vulnerability analysis from retrieved context through Groq.
- Serve health and chat endpoints through a FastAPI application.
- Evaluate retrieval against checked-in NVD and fused-corpus benchmarks, reporting Recall, Precision, nDCG, MRR, and R-Precision at configured cutoffs.
- Profile corpus metadata and write timestamped retrieval-evaluation reports.

## Architecture

```text
NVD CVE API + CISA KEV catalog
             |
   local raw JSON and normalization
             |
        KEV + NVD fusion
             |
     enriched retrieval chunks
             |
SentenceTransformers embeddings -> Pinecone (nvd / fused namespaces)
             |
query normalization, entity extraction, and CVE/CWE filtering
             |
dense retrieval -> cross-encoder reranking -> optional Groq grounded generation
             |
       FastAPI chat endpoint
```

## Repository layout

```text
packages/
  ingestion/       Source fetching, normalization, fusion, chunks, and local storage
  retrieval/       Embeddings, Pinecone access, query parsing, filters, and result models
                    plus cross-encoder reranking
  generation/      Groq client, prompts, and context formatting
  rag/             End-to-end retrieval and generation service
  evaluation/      Benchmarks, metrics, corpus analysis, and report models
apps/api/          FastAPI application, routers, dependencies, and response schemas
frontend/          React + Vite cybersecurity assistant interface
scripts/
  upsert_fused.py                  Embed and upload a corpus to Pinecone
  run_retrieval_evaluation.py      Evaluate nvd and fused namespaces
  inspect_corpus_metadata.py       Create a metadata completeness profile
  build_metadata_vocabulary.py     Build vendor/product vocabularies from chunks
tests/             Normalization tests
reports/retrieval/ Generated evaluation results
```

`data/` is intentionally ignored: it holds downloaded source data, normalized documents, chunks, and local metadata vocabularies.

## Setup

Requires Python 3.11+, a Pinecone index compatible with 384-dimensional cosine embeddings, and credentials for the services you use.

```powershell
pip install -e .
```

Create a `.env` file in the repository root:

```dotenv
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=bug-pattern-profiler
GROQ_API_KEY=your_groq_key
# Optional; defaults to llama3-70b-8192
GROQ_MODEL=llama3-70b-8192
# Optional: increases NVD API rate limits
NVD_API_KEY=your_nvd_key
```

All currently used runtime dependencies, including `sentence-transformers`, `torch`, `rapidfuzz`, FastAPI, and `pydantic-settings`, are declared in `pyproject.toml`.

## Run the pipeline

The current ingestion entry point normalizes existing raw files, creates NVD and KEV chunks, fuses KEV with NVD, and creates fused chunks:

```powershell
make ingest-local
```

Upload the fused chunks to Pinecone:

```powershell
python scripts/upsert_fused.py
```

The script is configured for the `fused` namespace. Its commented invocation shows how to upload the NVD collection to `nvd`.

## Query with RAG

```python
from packages.rag.rag_service import RAGService

rag = RAGService()
result = rag.answer(
    "What is CVE-2021-44228?",
    namespace="fused",
)

print(result["answer"])
for source in result["sources"]:
    print(source.cve_id, source.score)
```

RAG queries retrieve candidates from both `nvd` and `fused` namespaces, merge duplicate CVEs, and rerank the combined results before generating an answer. Queries such as `cve202144228` and `CWE 79` are normalized before retrieval. Exact CVE and CWE references become Pinecone filters; other query terms continue through dense semantic retrieval.

## Run the API

```powershell
uvicorn apps.api.app.main:app --reload
```

- `GET /health` returns the service status.
- `POST /chat` accepts a JSON body such as `{"query": "What is CVE-2021-44228?", "top_k": 5}` and returns the generated answer with its sources.

## Run the frontend

The `frontend/` directory contains a React 18, TypeScript, Vite, Tailwind CSS interface for the CyberRAG assistant. It renders structured vulnerability findings, including priority-ranked CVEs, remediation actions, patterns, hallucination flags, and source records.

Start the API first, then run the frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Vite serves the UI locally and proxies `POST /chat` requests to the FastAPI service at `http://localhost:8000`. For a production build:

```powershell
cd frontend
npm run build
```

The UI is responsive and has no persistent conversation store: New chat clears the active conversation.

## Run with Docker

Start the API and frontend together from the repository root:

```powershell
docker compose up --build
```

The frontend is available at `http://localhost:5173`, the API is available at `http://localhost:8000`, and the API documentation is at `http://localhost:8000/docs`. The frontend's `/chat` requests are proxied to the API service by Nginx.

To run the stack in the background and stop it later:

```powershell
docker compose up --build -d
docker compose down
```

The API container reads credentials and configuration from the root `.env` file. If an API container was started separately on port `8000`, stop it before running Compose.

## Evaluate retrieval

Run both checked-in benchmark suites:

```powershell
python scripts/run_retrieval_evaluation.py
```

The evaluator runs `nvd` and `fused` namespaces at `@10`, `@50`, and `@100`, summarizes results by ground-truth size, and writes JSON reports under `reports/retrieval/`.

### Evaluation snapshot

The latest recorded reranker evaluation (2026-07-27; 150 queries per namespace) shows stronger top-10 retrieval on the fused KEV+NVD collection than on the NVD-only collection.

| Namespace | Recall@10 | Precision@10 | nDCG@10 | MRR | R-Precision |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fused KEV+NVD | 0.3642 | 0.8993 | 0.9050 | 0.9441 | 0.7410 |
| NVD | 0.2066 | 0.8500 | 0.8542 | 0.9010 | 0.2600 |

Key observations:

- All six exact-CVE scenarios achieved perfect Recall@10, MRR, and R-Precision in both collections.
- The fused collection was especially effective for narrow ground-truth queries: Recall@10 was 0.8683, Precision@10 was 0.9300, and MRR was 0.9750.
- Broad queries show low Recall@10 (fused: 0.0300, NVD: 0.0003) because Recall@10 is capped at `10 / ground-truth size`, some scenarios match thousands of CVEs, so even perfect ranking can't score high. R-Precision (which scales the cutoff to ground-truth size) confirms fused broad queries retain reasonable ranking quality (0.2512), while NVD broad queries are genuinely weak (0.0027).
- These results show good early-ranking quality for focused lookups, while motivating the planned metadata filters, hybrid retrieval, and reranking for broad discovery queries.

To inspect corpus metadata completeness:

```powershell
python scripts/inspect_corpus_metadata.py
```

## Current limitations

- Retrieval is dense vector search followed by cross-encoder reranking; hybrid lexical retrieval is not implemented.
- Only CVE and CWE metadata filters are active. The parser extracts additional attributes, but severity, vendor, product, date, CVSS, and KEV-specific filters remain disabled.
- Vendor/product resolution requires local vocabulary files under `data/metadata/`; the vocabulary builder may need to be adjusted to produce the text-file format consumed by the resolver.
- Data fetching for NVD is currently commented out in the ingestion CLI, so that entry point expects locally stored raw NVD JSON.

## Data sources

- [NVD CVE API v2.0](https://services.nvd.nist.gov/rest/json/cves/2.0)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
