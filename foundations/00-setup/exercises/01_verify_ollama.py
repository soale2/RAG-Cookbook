"""
Exercise 1: Verify Ollama
=========================
Confirm Ollama is running and both required models are available.

Run:
    python exercises/01_verify_ollama.py
"""

import requests

OLLAMA_URL = "http://localhost:11434"
REQUIRED_MODELS = ["nomic-embed-text", "llama3.2"]


def get_available_models() -> list[str]:
    # TODO: GET /api/tags and return a list of model name strings.
    # The response JSON looks like: {"models": [{"name": "llama3.2:latest", ...}, ...]}
    # Hint: a model named "llama3.2:latest" should match the requirement "llama3.2"
    pass


def main():
    print("Checking Ollama connection...")
    try:
        models = get_available_models()
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Ollama.")
        print("       Start it with: ollama serve")
        return

    print(f"Found {len(models)} model(s) installed.\n")

    all_ok = True
    for required in REQUIRED_MODELS:
        found = any(required in m for m in models)
        if found:
            print(f"  OK  {required}")
        else:
            print(f"  MISSING  {required}")
            print(f"           Run: ollama pull {required}")
            all_ok = False

    print()
    if all_ok:
        print("All models ready. Move on to Exercise 2.")
    else:
        print("Pull the missing models, then re-run this script.")


if __name__ == "__main__":
    main()
