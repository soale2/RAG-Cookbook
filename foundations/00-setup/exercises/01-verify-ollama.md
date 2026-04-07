---
slug: /00-setup/exercises/01-verify-ollama
---

# Exercise 1 - Verify Ollama

> **Goal:** Confirm Ollama is running and the two models you need are available.

---

## Before you start

Make sure you have run:

```bash
ollama serve
ollama pull nomic-embed-text
ollama pull llama3.2
```

---

## Assignment

Open `01_verify_ollama.py` and work through the following steps:

1. Send a GET request to `http://localhost:11434/api/tags` and print the response.
2. Parse the JSON and extract just the model names from the list.
3. Check that both `nomic-embed-text` and `llama3.2` appear in that list. Print a clear pass/fail message for each.
4. If a model is missing, print the exact `ollama pull` command the user needs to run.

Run it:

```bash
python exercises/01_verify_ollama.py
```

You should see two green-light messages. If you see a connection error, Ollama is not running - start it with `ollama serve`.

---

## Thinking questions

- What HTTP status code do you get from `/api/tags` when Ollama is running? What do you get when it is not?
- What does the full JSON response look like? What other information is in it besides model names?

---

[Next: Exercise 2 - First API Calls →](./02-first-calls)
