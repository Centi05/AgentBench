# AgentBench — Week 1: Document Ingestion & Semantic Search

**Goal:** Build a reproducible pipeline that loads technical documentation (PDF, Markdown, TXT), extracts text, chunks it, generates embeddings, indexes vectors in Qdrant, and retrieves relevant passages with source metadata.

**Status:** ⬜ Not started / 🟡 In progress / ✅ Complete (update as work progresses)

> **Definition of done:** A fresh clone can follow the README, run automated tests, ingest a sample document, and execute a natural-language similarity query with identifiable source passages. No secrets or virtual environments are committed.

## Milestone 1 — Repository and Python environment

**Suggested GitHub label:** `week-1`, `setup`  
**Files:** `.gitignore`, `.env.example`, `requirements.txt`, `README.md`

- [ ] Confirm the GitHub repository clones successfully on Windows.
- [ ] Open the repository root in VS Code; verify terminal working directory.
- [ ] Install a supported Python version (target 3.11 or 3.12) and confirm `python --version`.
- [ ] Create `.venv` inside the repository and select it as the VS Code interpreter.
- [ ] Upgrade pip and install `requirements.txt` without errors.
- [ ] Verify imports for `sentence_transformers`, `qdrant_client`, `pymupdf`, `dotenv`, and `pytest`.
- [ ] Confirm `.gitignore` excludes `.venv/`, `.env`, Python caches, and local artifacts.
- [ ] Create `.env` from `.env.example`; keep credentials out of Git.
- [ ] Record Python version and dependency installation instructions in README.

**Acceptance checks**
- [ ] `python -m pip check` succeeds.
- [ ] Import smoke test succeeds inside `.venv`.
- [ ] `git status` does not show `.venv/` or `.env` as untracked/staged.

## Milestone 2 — Research and architecture

**Suggested labels:** `week-1`, `documentation`, `research`

- [ ] Read or skim Sentence-BERT (Reimers & Gurevych, EMNLP 2019).
- [ ] Read or skim Dense Passage Retrieval (Karpukhin et al., EMNLP 2020).
- [ ] Review fixed-size versus semantic chunking and document a baseline choice.
- [ ] Review HNSW at a conceptual level and explain approximate nearest-neighbor search.
- [ ] Draw a pipeline diagram: files → parser → chunks → embeddings → Qdrant → query.
- [ ] Document why the baseline uses `all-MiniLM-L6-v2` and its 384-dimensional vectors.
- [ ] Record initial chunk-size and overlap configuration and the units used (characters versus tokens).
- [ ] Define document/chunk metadata fields: source path, document ID, chunk ID, chunk index, page number when available.
- [ ] Record assumptions and limitations (scanned PDFs, tables, code blocks, CPU inference).

**Acceptance checks**
- [ ] README or `docs/architecture.md` explains each component and its interfaces.
- [ ] Config values are documented and can be changed without editing core pipeline logic.

## Milestone 3 — Document loading and extraction

**Suggested labels:** `week-1`, `feature`, `ingestion`  
**Files:** `app/document_loader.py`, `tests/test_document_loader.py`

- [ ] Load UTF-8 `.txt` files.
- [ ] Load `.md` files without losing heading text or code samples.
- [ ] Extract selectable text from `.pdf` files with PyMuPDF.
- [ ] Preserve PDF page numbers and source filenames in metadata.
- [ ] Traverse a directory and identify supported file extensions.
- [ ] Skip unsupported files with an informative message.
- [ ] Handle empty files, corrupt PDFs, and decoding errors without silently ingesting garbage.
- [ ] Normalize whitespace conservatively; avoid damaging code snippets and command examples.
- [ ] Test at least one file of each supported format.

**Acceptance checks**
- [ ] Sample TXT, Markdown, and PDF content can be inspected after loading.
- [ ] Every extracted unit includes a source reference; PDF units include page numbers where applicable.
- [ ] Tests cover successful extraction and at least one invalid/empty-file case.

## Milestone 4 — Text preprocessing and chunking

**Suggested labels:** `week-1`, `feature`, `chunking`  
**Files:** `app/chunker.py`, `tests/test_chunker.py`

- [ ] Implement configurable chunk size and overlap.
- [ ] Validate parameters: chunk size > 0 and 0 ≤ overlap < chunk size.
- [ ] Keep chunks in original document order.
- [ ] Preserve source metadata for every chunk.
- [ ] Assign deterministic chunk IDs (or document ID + index) to support repeatable ingestion.
- [ ] Handle documents shorter than one chunk and empty input.
- [ ] Avoid creating empty or whitespace-only chunks.
- [ ] Confirm adjacent chunks overlap as configured.
- [ ] Inspect whether chunks split headings, commands, or code blocks in undesirable places; record known limitations.

**Acceptance checks**
- [ ] Automated tests pass for empty, short, long, and boundary-length inputs.
- [ ] Chunk IDs and metadata are stable across identical runs.
- [ ] A sample document produces nonempty, correctly ordered chunks.

## Milestone 5 — Embedding generation

**Suggested labels:** `week-1`, `feature`, `ml`  
**Files:** `app/embeddings.py`

- [ ] Load `sentence-transformers/all-MiniLM-L6-v2` successfully.
- [ ] Generate embeddings for a small list of sample sentences.
- [ ] Confirm shape `(number_of_chunks, 384)`.
- [ ] Check vectors contain only finite numeric values (no NaN/Inf).
- [ ] Support batched encoding rather than encoding every chunk separately.
- [ ] Record model identifier and embedding dimension in configuration.
- [ ] Compare similarity for related versus unrelated technical sentences as a sanity check.
- [ ] Document CPU support and first-run model download behavior.

**Acceptance checks**
- [ ] Three test sentences produce a `(3, 384)` embedding matrix.
- [ ] Embedding dimension matches the configured Qdrant collection size.
- [ ] A basic semantic similarity smoke test returns plausible ordering (not a guaranteed accuracy metric).

## Milestone 6 — Qdrant vector storage

**Suggested labels:** `week-1`, `feature`, `database`  
**Files:** `docker-compose.yml`, `app/vector_store.py`

- [ ] Install and start Docker Desktop.
- [ ] Launch Qdrant with `docker compose up -d`.
- [ ] Confirm the Qdrant health endpoint or dashboard is reachable at localhost port 6333.
- [ ] Create a collection with vector size 384 and the selected distance metric.
- [ ] Upsert chunks with embeddings and source metadata as payload.
- [ ] Query top-k similar vectors with a natural-language query embedding.
- [ ] Return scores, passage text, and source metadata.
- [ ] Decide and document repeated-ingestion behavior (idempotent update vs duplicates).
- [ ] Verify persistent storage survives a container restart.
- [ ] Provide actionable errors if Qdrant is unavailable or vector dimensions mismatch.

**Acceptance checks**
- [ ] Qdrant collection appears in the dashboard.
- [ ] Point count matches expected unique chunks after ingestion.
- [ ] Reingesting unchanged files does not unexpectedly duplicate entries.
- [ ] Query results include source references and scores.

## Milestone 7 — End-to-end ingestion and search

**Suggested labels:** `week-1`, `integration`  
**Files:** `app/ingest.py`, `data/raw/`

- [ ] Add a small, legally shareable sample technical document corpus.
- [ ] Provide a CLI command for ingesting `data/raw/`.
- [ ] Print useful ingestion counts: files loaded, extracted units, chunks generated, vectors stored.
- [ ] Add a CLI query option for semantic search.
- [ ] Run a known-answer query such as “What does DHCP configure?” against the sample docs.
- [ ] Display top-k passages with scores, filenames, and page/chunk identifiers.
- [ ] Check that answers about distinct topics retrieve different relevant passages.
- [ ] Validate failure behavior for missing directory, empty corpus, and stopped Qdrant container.
- [ ] Capture a terminal screenshot or sample output for the README.

**Acceptance checks**
- [ ] One documented command ingests the sample corpus.
- [ ] One documented command retrieves relevant source passages.
- [ ] End-to-end run completes without exceptions on a clean environment.

## Milestone 8 — Tests, documentation, and GitHub delivery

**Suggested labels:** `week-1`, `testing`, `documentation`

- [ ] Run `python -m pytest -q` and fix failures.
- [ ] Add tests for loader, chunker, and metadata handling.
- [ ] Add at least one integration smoke test (can be marked as requiring local Qdrant).
- [ ] Run `python -m pip check`.
- [ ] Review exceptions and error messages for common setup failures.
- [ ] Write README prerequisites: Python, Docker, VS Code optional.
- [ ] Document environment setup, Qdrant startup, ingestion, querying, and tests.
- [ ] Document expected outputs and troubleshooting for Windows PowerShell.
- [ ] Add a short architecture diagram and describe current limitations.
- [ ] Confirm no secrets, `.env`, `.venv`, downloaded model weights, or large datasets are staged.
- [ ] Commit Week 1 work and push to GitHub.
- [ ] Create a GitHub milestone or Project board view to track follow-on weeks.

**Acceptance checks**
- [ ] All unit tests pass; integration test passes when Docker/Qdrant is running.
- [ ] A fresh clone can reproduce the pipeline using the README.
- [ ] GitHub repository contains code, docs, and safe example configuration.

---

## Recommended GitHub Project columns

- **Backlog** — Not started
- **Ready** — Defined and ready to pick up
- **In Progress** — Currently implementing
- **Blocked** — Waiting on dependency or debugging
- **In Review** — Code complete; awaiting validation
- **Done** — Acceptance checks passed

## Suggested issue titles

1. `[W1-01] Configure repository, Python environment, and dependencies`
2. `[W1-02] Document architecture and retrieval research decisions`
3. `[W1-03] Implement technical document loaders`
4. `[W1-04] Implement configurable chunking and metadata`
5. `[W1-05] Generate and validate sentence embeddings`
6. `[W1-06] Integrate Qdrant vector storage and similarity search`
7. `[W1-07] Run end-to-end ingestion and query smoke test`
8. `[W1-08] Complete tests, documentation, and GitHub release`

## Dependencies / recommended order

`W1-01 → W1-03 → W1-04 → W1-05 → W1-06 → W1-07 → W1-08`

`W1-02` can run in parallel with setup and implementation.

## Optional stretch goals (not required for Week 1)

- [ ] Benchmark 256-, 512-, and 1024-token chunking variants **after implementing token-aware splitting**.
- [ ] Compare two embedding models with matched retrieval evaluation data.
- [ ] Add incremental ingestion based on document content hashes.
- [ ] Add GitHub Actions for unit tests that do not require Docker.
- [ ] Add a small labeled query set for Week 3 retrieval evaluation.

**Out of scope for Week 1:** LLM answer generation, agent tool calling, RAGAS scoring, React dashboard, and cloud deployment.
