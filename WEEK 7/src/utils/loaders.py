import os
from pathlib import Path

import pandas as pd
from docx import Document
import fitz  # PyMuPDF


def load_documents(base_dir: Path):

    docs = []

    for path in base_dir.rglob("*"):

        if path.suffix.lower() == ".pdf":
            docs.extend(load_pdf(path))

        elif path.suffix.lower() == ".txt":
            docs.append({
                "text": path.read_text(errors="ignore"),
                "source": str(path),
                "page": None,
                "tags": []
            })

        elif path.suffix.lower() == ".csv":
            df = pd.read_csv(path)
            for i, row in df.iterrows():
                docs.append({
                    "text": " ".join(map(str, row.values)),
                    "source": str(path),
                    "page": int(i),
                    "tags": []
                })

        elif path.suffix.lower() == ".docx":
            docs.append(load_docx(path))

    return docs


def load_pdf(path):

    doc = fitz.open(path)
    pages = []

    for i, page in enumerate(doc):
        pages.append({
            "text": page.get_text(),
            "source": str(path),
            "page": i,
            "tags": []
        })

    return pages


def load_docx(path):

    doc = Document(path)
    full = []

    for p in doc.paragraphs:
        full.append(p.text)

    return {
        "text": "\n".join(full),
        "source": str(path),
        "page": None,
        "tags": []
    }
