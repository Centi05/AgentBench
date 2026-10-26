# AgentBench — Week 1

Technical-document ingestion, semantic embeddings, and Qdrant vector search.

## Requirements
- Python 3.11+
- Docker Desktop (or Docker Engine with Compose)
- Internet access on first run to download the embedding model

## Setup
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env  # Windows PowerShell: Copy-Item .env.example .env
docker compose up -d
```

## Ingest and test retrieval
```bash
python -m app.ingest --directory data/raw --query "What does DHCP configure?"
python -m pytest -q
```

Place your own .pdf, .md, or .txt files under `data/raw/`. Ingestion upserts stable IDs based on source/page/chunk index. Note: changing chunking settings or removing files can leave stale points; reset the collection when benchmarking new chunking strategies. Source paths are stored as metadata; avoid uploading private files to shared databases. PDFs with scanned images need OCR, which is not included in Week 1.

## Planned next steps
Week 2: hybrid retrieval, source citations, FastAPI answer endpoint.
Week 3: labeled evaluation dataset, recall@k, MRR, groundedness.
Week 4: LangGraph agent and tool execution traces.
Weeks 5–6: dashboard, experiments, monitoring, deployment.
