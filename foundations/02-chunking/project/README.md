---
slug: /02-chunking/project
---

# Project: Document Processor

> Build a pipeline that loads documents from disk and splits them into overlapping chunks ready for embedding.

---

## Brief

The exercises had you chunking hardcoded strings. Now build a real pipeline that works on actual files: PDFs, plain text, and Word documents.

Your pipeline should have three parts:

1. **Config** - a settings object (use Pydantic or a plain dataclass) with chunk size, overlap, model names, and any paths. Load from environment variables or a `.env` file.

2. **Document loader** - a function that takes a folder path and returns a list of documents with metadata (source filename, file type). Support at least `.pdf` and `.txt`. Use LangChain loaders or raw Python.

3. **Text splitter** - a function that takes the loaded documents and splits them into chunks with configurable size and overlap. Preserve the source metadata on every chunk.

---

## Example output

```
Found 3 file(s) in ./papers
Loaded 12 page(s) from attention.pdf
Loaded 8 page(s) from bert.pdf
Loaded 1 page(s) from notes.txt
Split 21 document(s) into 147 chunks

Stats:
  total_chunks: 147
  avg_chunk_size: 824
  min_chunk_size: 102
  max_chunk_size: 1000
  chunks_per_source: {'attention.pdf': 68, 'bert.pdf': 61, 'notes.txt': 18}
```

---

## Requirements

- [ ] Load `.pdf` and `.txt` files from a folder (recursively)
- [ ] Inject `source` and `file_type` metadata on every document
- [ ] Split with configurable `chunk_size` and `chunk_overlap`
- [ ] Print chunk statistics (count, avg/min/max size, per-source breakdown)
- [ ] Skip unsupported file types with a warning, not a crash

## Stretch goals

- Add `.docx`, `.html`, or `.csv` loaders
- Write a `get_chunk_stats()` utility that returns a dict for programmatic use
- Experiment with different chunk sizes and compare the stats
