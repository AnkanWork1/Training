from pathlib import Path

def load_enterprise_markdown(root_dir: Path):
    """
    Load markdown documents folder-wise.
    Each folder = one document (one PDF).
    Returns list of dicts with text + metadata.
    """
    documents = []

    for doc_dir in sorted(root_dir.iterdir()):
        if not doc_dir.is_dir():
            continue

        doc_id = doc_dir.name
        md_file = doc_dir / f"{doc_id}.md"
        json_file = doc_dir / f"{doc_id}.json"

        if not md_file.exists():
            continue

        text = md_file.read_text(encoding="utf-8", errors="ignore")

        image_files = []
        for ext in ("*.png", "*.jpg", "*.jpeg"):
            image_files.extend(doc_dir.glob(ext))

        documents.append(
            {
                "text": text,
                "metadata": {
                    "doc_id": doc_id,
                    "md_path": str(md_file),
                    "json_path": str(json_file) if json_file.exists() else None,
                    "image_paths": [str(p) for p in image_files],
                    "source_pdf": str(md_file.parent.parent / f"{doc_id}.pdf")  # <-- fixed
                }
            }
        )

    return documents
