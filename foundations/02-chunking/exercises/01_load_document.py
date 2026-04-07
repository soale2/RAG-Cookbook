"""
Exercise 1: Load a Document
============================
Load a PDF and a text file. Inspect the raw content and metadata.

Run:
    python exercises/01_load_document.py

Prerequisites:
    pip install langchain langchain-community pypdf
"""

from pathlib import Path


def load_pdf(path: str):
    # TODO: Use PyPDFLoader to load the file and return the list of Documents.
    # from langchain_community.document_loaders import PyPDFLoader
    pass


def load_txt(path: str):
    # TODO: Use TextLoader to load the file and return the list of Documents.
    # from langchain_community.document_loaders import TextLoader
    pass


def inspect(docs, label: str):
    print(f"\n=== {label} ===")
    # TODO:
    # 1. Print how many documents (pages) were returned.
    # 2. Print the metadata of the first document.
    # 3. Print the first 500 characters of the first document's page_content.
    pass


if __name__ == "__main__":
    # Find a PDF in data/papers/ (adjust the path if needed)
    papers_dir = Path("data/papers")
    pdfs = list(papers_dir.glob("*.pdf"))
    if not pdfs:
        print("No PDFs found in data/papers/. Add a PDF there and re-run.")
    else:
        pdf_docs = load_pdf(str(pdfs[0]))
        inspect(pdf_docs, f"PDF: {pdfs[0].name}")

    # Also try a plain text file if one exists
    txts = list(papers_dir.glob("*.txt"))
    if txts:
        txt_docs = load_txt(str(txts[0]))
        inspect(txt_docs, f"TXT: {txts[0].name}")
    else:
        print("\nNo .txt files found. Try creating one and loading it.")
