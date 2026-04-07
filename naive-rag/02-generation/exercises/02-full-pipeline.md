---
slug: /02-generation/exercises/02-full-pipeline
---

# Exercise 2 — Full Pipeline

> **Goal:** Wire retrieval and generation into a single `ask(question)` function. You now have a complete, working naive RAG system.

---

## Background

You have all the pieces:

- FAISS index with embedded chunks (Foundations 03)
- A retriever that returns top-k chunks (Naive RAG 01)
- A prompt builder that grounds the LLM (this module, Exercise 1)

This exercise combines them into one callable pipeline.

---

## Assignment

Open `02_full_pipeline.py`.

1. Load your FAISS index and chunks.
2. Write `ask(question, k=5)` that:
   - Retrieves top-k chunks for the question
   - Builds the strict prompt from Exercise 1
   - Calls `llama3.2` for the answer
   - Returns the answer string
3. Run it against at least 5 questions — mix of in-corpus and out-of-corpus.
4. For each answer, also print which chunks were retrieved (the first 80 chars of each). Verify the answer is supported by what was retrieved.

**Stretch:** Add a `verbose=True` parameter to `ask` that prints the full prompt before sending it to the model. Read the prompt carefully — does it look the way you expect?

---

## Thinking questions

- You built the index once (in Foundations) and reuse it here. In a real application, when would you need to rebuild it?
- Your pipeline makes two network calls per question: one to the embedding endpoint, one to the generation endpoint. Which is slower? Does it matter?
- If the retriever returns a wrong chunk (low quality retrieval), the generator will produce a wrong answer confidently. What would you add to this pipeline to catch that?

---

[← Exercise 1](./01-build-prompt) · [Next: 03 Cloud Models →](../../03-cloud-models/exercises/01-gemini-call)
