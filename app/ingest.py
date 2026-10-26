import argparse
from pathlib import Path
from app.config import Settings
from app.document_loader import load_directory
from app.chunker import chunk_pages
from app.embeddings import Embedder
from app.vector_store import VectorStore

def main():
    parser = argparse.ArgumentParser(description="AgentBench Week 1: ingest and search docs")
    parser.add_argument("--directory", default="data/raw")
    parser.add_argument("--query", help="Run a semantic search after ingestion")
    args = parser.parse_args()
    cfg = Settings()
    pages = load_directory(Path(args.directory))
    chunks = chunk_pages(pages, cfg.chunk_size, cfg.chunk_overlap)
    print(f"Loaded {len(pages)} document pages/sections; generated {len(chunks)} chunks")
    if not chunks:
        print("No supported documents found. Add PDF, MD, or TXT files to data/raw.")
        return
    embedder = Embedder(cfg.embedding_model)
    vectors = embedder.encode([c.text for c in chunks])
    store = VectorStore(cfg.qdrant_url, cfg.collection, embedder.dimension)
    store.upsert(chunks, vectors)
    print(f"Upserted {len(chunks)} vectors into {cfg.collection}")
    if args.query:
        results = store.search(embedder.encode([args.query])[0])
        for i, hit in enumerate(results, 1):
            p = hit.payload
            print(f"\n{i}. score={hit.score:.3f} source={p['source']} page={p['page_number']}\n{p['text'][:400]}")

if __name__ == "__main__":
    main()
