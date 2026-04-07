# RAG Complete Study Guide

A structured, hands-on curriculum for building Retrieval-Augmented Generation (RAG) systems - for Python developers who want to understand RAG from the ground up.

Each module combines theory, exercises, and a project. The projects are **cumulative** within each track - by the end you have a fully working pipeline.

---

## How to use this guide

1. Start with **Foundations** - the building blocks every RAG variant depends on.
2. Pick a **track** and work through it in order.
3. Read the theory in each module's `README.md`, complete the exercises, then tackle the project.

---

## Foundations

Core concepts shared across all RAG variants.

| Module | Topic |
|--------|-------|
| [00 - Setup](./foundations/00-setup/) | Environment, Ollama, tooling |
| [01 - Embeddings](./foundations/01-embeddings/) | Vector spaces, similarity, normalization |
| [02 - Chunking](./foundations/02-chunking/) | Document loading, text splitting |
| [03 - Vector Stores](./foundations/03-vector-stores/) | FAISS, ChromaDB, indexing algorithms |

## Tracks

| Track | Description | Status |
|-------|-------------|--------|
| [Naive RAG](./naive-rag/) | The baseline pipeline: retrieve chunks, generate an answer | In progress |
| [Advanced RAG](./advanced-rag/) | Query rewriting, hybrid search, reranking | Coming soon |
| [Agentic RAG](./agentic-rag/) | LLM-driven retrieval with tool use | Coming soon |
| [Graph RAG](./graph-rag/) | Retrieval over knowledge graphs | Coming soon |

---

## Reference implementations

Completed, working examples are in [`reference/`](./reference/) - use these to compare against your own work.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

You will also need [Ollama](https://ollama.com/) installed locally:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

## Sample papers

Foundational RAG papers are in [`data/papers/`](./data/papers/) for use across exercises and projects.
