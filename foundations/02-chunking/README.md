---
slug: /02-chunking
---

# 02 - Chunking

> **Goal:** Understand why documents must be split before indexing, how different splitting strategies affect retrieval quality, and how to preserve metadata across chunks.

---

## Theory

### Why chunking is necessary

An embedding model compresses an entire input into a fixed-size vector - 768 numbers, regardless of whether you feed it a single sentence or a ten-page document. When you embed a long document, the vector averages out all the meaning. A query about one specific claim in that document will produce a vector that only weakly matches the full-document embedding, because the match is diluted by everything else in the document.

The solution is to split documents into smaller pieces - **chunks** - and embed each chunk independently. Now a query can match the specific chunk that contains the relevant claim, not a blurry average of the whole document.

```
Document (10 pages)         →  one blurry vector
Chunks   (20 × ~500 chars)  →  20 precise vectors
```

The trade-off: smaller chunks are more precise but lose surrounding context. Larger chunks preserve context but dilute the signal. Choosing chunk size is one of the most impactful tuning decisions in a RAG pipeline.

---

### Fixed-size chunking

The simplest approach: split on character count, with optional overlap.

```python
def split(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

**Overlap** repeats the last `overlap` characters of each chunk at the start of the next. This prevents a sentence being cut in half at a boundary, losing its meaning. A 10–20% overlap is typical.

The downside of naive fixed-size splitting: it ignores structure. It will split mid-sentence, mid-paragraph, even mid-word.

---

### Recursive character splitting

A better approach: try to split on natural boundaries first, fall back to smaller ones only when necessary.

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""],
)
chunks = splitter.split_text(document_text)
```

The splitter tries `\n\n` (paragraph breaks) first. If a resulting piece is still over `chunk_size`, it tries `\n`, then `. `, then ` `, then individual characters as a last resort. This produces chunks that respect document structure as much as possible while staying within the size limit.

This is the default strategy for most RAG pipelines and what you should reach for first.

---

### Chunk size trade-offs

| Chunk size | Retrieval precision | Context per chunk | Risk |
|-----------|--------------------|--------------------|------|
| Small (~200 chars) | High | Low - may miss surrounding context | Fragments ideas |
| Medium (~500 chars) | Good | Good | Reasonable for most tasks |
| Large (~1500 chars) | Lower | High | Dilutes signal, may exceed model context |

Start with 500 characters and 100 overlap. Measure retrieval quality (does the right chunk come back for your test queries?), then adjust.

---

### Document loading

Before you can chunk, you need text. Different file formats need different loaders:

```python
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def load(path: str):
    if path.endswith(".pdf"):
        return PyPDFLoader(path).load()
    elif path.endswith(".txt"):
        return TextLoader(path).load()
    raise ValueError(f"Unsupported format: {path}")
```

Each loader returns a list of `Document` objects. Each `Document` has `.page_content` (the text) and `.metadata` (source path, page number, etc.).

---

### Preserving metadata

Metadata is how you trace a retrieved chunk back to its source. Always carry it through the pipeline:

```python
def split_documents(docs, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = []
    for doc in docs:
        pieces = splitter.split_text(doc.page_content)
        for i, piece in enumerate(pieces):
            chunks.append({
                "text": piece,
                "metadata": {**doc.metadata, "chunk_index": i},
            })
    return chunks
```

When the pipeline returns a chunk to the user, the `metadata` tells you which document and which page it came from. Without this, your RAG system cannot cite its sources.

---

### Key takeaways

- Embed chunks, not full documents. Full-document embeddings average out meaning and hurt retrieval precision.
- Recursive character splitting respects document structure. Use it over naive character splitting.
- Overlap (~10–20%) prevents information loss at chunk boundaries.
- Start with 500-char chunks and tune based on retrieval quality, not intuition.
- Always preserve source metadata on every chunk. You will need it for citations and debugging.

---

## Exercises

1. [Load a Document](./exercises/01-load-document) - use Langchain loaders and inspect raw text and metadata
2. [Split Text](./exercises/02-split-text) - chunk a document and confirm overlap works as expected
3. [Chunk Size Trade-offs](./exercises/03-chunk-size) - compare retrieval precision across three chunk sizes

---

## Project - Part 2

See [`project/`](./project/).

---

[← 01 Embeddings](../01-embeddings/) · [03 Vector Stores →](../03-vector-stores/)
