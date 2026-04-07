---
slug: /02-generation/exercises/01-build-prompt
---

# Exercise 1 — Build a RAG Prompt

> **Goal:** Write a prompt function that grounds the LLM in retrieved context, and learn exactly why prompt wording determines faithfulness.

---

## Background

A RAG prompt has one job: give the model the context it needs and instruct it to stay within that context. The difference between "answer based on the context" and "answer using only the context" is the difference between a grounded answer and a hallucination.

---

## Assignment

Open `01_build_prompt.py`.

1. Write a `build_prompt(context_chunks, question)` function. Format the chunks with clear separators so the model can tell where one chunk ends and another begins.
2. Test three versions of the instruction:
   - **Loose:** `"Answer the question using the context below."`
   - **Strict:** `"Answer using only the information in the context. If the answer is not there, say so."`
   - **Explicit fallback:** Same as strict, but add: `"Do not use any knowledge outside the context."`
3. For each version, call `llama3.2` with the same context and the same question. Use a question where you know the answer is in the context.
4. Now ask a question where the answer is NOT in the context. Which instruction version makes the model say "I don't know"? Which lets it hallucinate?

---

## Thinking questions

- The model "knows" many facts from training. What instruction phrasing most reliably prevents it from using that knowledge?
- If you have 8 context chunks, does the order you put them in the prompt matter? Try putting the most relevant chunk first vs. last.
- How would you test whether a model's answer is faithful to the context without reading both manually?

---

[Next: Exercise 2 — Full Pipeline →](./02-full-pipeline)
