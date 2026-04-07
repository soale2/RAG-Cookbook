---
slug: /00-setup/exercises/02-first-calls
---

# Exercise 2 — First API Calls

> **Goal:** Make a real embedding call and a real generation call. Confirm both return sensible output.

---

## Background

Ollama exposes two endpoints you will use throughout this curriculum:

- `POST /api/embeddings` — converts text to a vector
- `POST /api/generate` — generates text given a prompt

Both are simple JSON over HTTP. No SDK required.

---

## Assignment

Open `02_first_calls.py`.

**Part A — Embeddings**

1. Call `/api/embeddings` with the model `nomic-embed-text` and any short sentence.
2. Convert the returned list to a `numpy` float32 array.
3. Print the shape. It should be `(768,)`.
4. Print the min, max, and L2 norm of the raw vector.

**Part B — Generation**

1. Call `/api/generate` with the model `llama3.2`, a simple question as the prompt, and `"stream": false`.
2. Print the `"response"` field from the JSON.
3. Time how long the call takes using `time.time()`. Print the duration.

**Part C — Reflect**

Add a comment at the bottom of the file answering:
- Is the embedding vector already normalised (norm ≈ 1.0)?
- How many seconds did generation take on your machine?

---

## Thinking questions

- What happens if you pass an empty string to the embedding endpoint?
- The generation endpoint also accepts `"stream": true` (the default). What would you need to change in your code to handle a streamed response?

---

[← Exercise 1](./01-verify-ollama) · [Next: 01 Embeddings →](../../01-embeddings/exercises/01-first-embedding)
