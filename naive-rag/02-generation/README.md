---
slug: /02-generation
---

# 02 - Generation

> **Goal:** Wire the LLM into the retrieval pipeline. Learn how to write prompts that produce faithful, grounded answers, understand why RAG reduces hallucination, and complete the end-to-end Q&A loop.

---

## Theory

### The generation step

Retrieval finds the relevant chunks. Generation turns those chunks into an answer. The two steps together form the complete RAG pipeline:

```
query
  └─► embed ─► vector search ─► top-k chunks
                                      └─► build prompt ─► LLM ─► answer
```

The LLM never sees the full document corpus - only the small set of chunks the retriever selected. This is the key insight of RAG: you give the model the context it needs, just in time, rather than hoping it memorised the right facts during training.

---

### Why RAG reduces hallucination

A plain LLM generates answers from its training weights. When it does not know the answer, it often generates something plausible-sounding but wrong - a hallucination.

RAG grounds the model by placing the relevant source text directly in the prompt. The model can then quote or paraphrase the context rather than inventing an answer. It can also say "I don't know" when the retrieved context does not contain the answer.

This only works if:
1. The retriever returns the relevant chunk (retrieval quality)
2. The prompt instructs the model to stay within the provided context (prompt design)
3. The model is capable of following that instruction (model capability)

If any of these fail, hallucination returns. Better retrieval and better prompts are always worth addressing before switching to a bigger model.

---

### Prompt structure

A RAG prompt has three parts: an instruction, the retrieved context, and the user's question.

```python
def build_prompt(context_chunks: list[str], question: str) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    return f"""You are a helpful assistant. Answer the question using only the context below.
If the context does not contain enough information to answer, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}

Answer:"""
```

The instruction matters. Without "using only the context below", the model mixes retrieved facts with memorised knowledge and you cannot tell which is which.

---

### The full Q&A loop

```python
import requests

def ask(question: str, index, chunks: list[str], k: int = 5) -> str:
    # 1. Retrieve
    top_chunks = retrieve(question, index, chunks, k=k)
    context = [c["text"] for c in top_chunks]

    # 2. Build prompt
    prompt = build_prompt(context, question)

    # 3. Generate
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=120,
    )
    return response.json()["response"].strip()
```

This is a complete naive RAG pipeline in under 20 lines. Everything you build on top of this - reranking, query rewriting, evaluation - is an improvement to one of these three steps.

---

### Context window limits

LLMs have a maximum context length (measured in tokens). `llama3.2` supports 128k tokens, but longer prompts are slower and the model's attention weakens on content far from the question.

A practical rule: keep the total prompt under 4,000 tokens for fast local inference. At ~4 characters per token, that is roughly 16,000 characters. Five 500-character chunks plus a system prompt fits comfortably.

If you find yourself pushing against context limits, the answer is better retrieval (return fewer, more relevant chunks), not a larger context window.

---

### Faithfulness vs fluency

Two separate things can go wrong with generation:

**Faithfulness:** Is the answer grounded in the retrieved context? A faithful answer only states things that appear in the provided chunks.

**Fluency:** Is the answer well-written and coherent? A fluent answer reads naturally, even if it is wrong.

LLMs are almost always fluent. Faithfulness is the harder problem. You can test faithfulness by asking: "Does every factual claim in this answer appear in the context?"

The simplest way to improve faithfulness is to make the instruction more explicit:

```python
# Less explicit
"Answer the question based on the context."

# More explicit
"Answer the question using only the information in the context. 
Do not add information that is not in the context. 
If the answer is not in the context, say so."
```

---

### Handling "I don't know"

A good RAG system declines gracefully when the corpus does not contain the answer. Build this in from the start:

```python
NO_ANSWER_PHRASES = [
    "i don't have enough information",
    "the context does not",
    "not mentioned in the",
    "cannot find",
]

def has_answer(response: str) -> bool:
    return not any(p in response.lower() for p in NO_ANSWER_PHRASES)
```

This is not foolproof - a model can hallucinate confidently - but it is a starting point. Module 02 of Advanced RAG covers proper faithfulness evaluation.

---

### Key takeaways

- Generation takes the retrieved chunks and produces a natural language answer.
- RAG reduces hallucination by placing source text in the prompt, but only if the prompt instructs the model to stay within it.
- The full pipeline is: embed query, retrieve top-k, build prompt, generate. That is it.
- Keep prompts under ~4,000 tokens for fast local inference. Better retrieval beats bigger context windows.
- Fluency is easy. Faithfulness - staying grounded in the retrieved context - is the hard part.

---

## Exercises

1. [Build a RAG Prompt](./exercises/01-build-prompt) - test how prompt wording controls faithfulness
2. [Full Pipeline](./exercises/02-full-pipeline) - wire retrieval and generation into a working `ask()` function

---

## Project - Part 2 (Naive RAG)

See [`project/`](./project/).

---

[← 01 Retrieval](../01-retrieval/) · [03 Cloud Models →](../03-cloud-models/)
