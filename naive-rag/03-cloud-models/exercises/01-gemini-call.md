---
slug: /03-cloud-models/exercises/01-gemini-call
---

# Exercise 1 — Your First Gemini Call

> **Goal:** Get the Gemini API working and compare its output to `llama3.2` on the same prompt.

---

## Before you start

You need an API key from [Google AI Studio](https://aistudio.google.com/). It is free. Store it in your environment — never in code:

```bash
export GEMINI_API_KEY="your-key-here"
```

Install the SDK:

```bash
pip install google-generativeai
```

---

## Assignment

Open `01_gemini_call.py`.

1. Write a `generate_gemini(prompt)` function using `google.generativeai` with model `gemini-2.0-flash`.
2. Write a `generate_ollama(prompt)` function using the Ollama HTTP API with `llama3.2`.
3. Run both on the same three prompts:
   - A factual question with a clear answer
   - A request to summarise a short paragraph
   - An out-of-context question with no good answer
4. Print both responses side by side for each prompt.
5. Time each call. Print the latency.

---

## Thinking questions

- Did the two models give the same answer? Different answers? Which felt more accurate?
- Gemini was faster or slower than your local `llama3.2`? What does that depend on?
- Your API key is in an environment variable. What would happen if you accidentally committed a file that contained the key as a string?

---

[Next: Exercise 2 — Swap the Generator →](./02-swap-generator)
