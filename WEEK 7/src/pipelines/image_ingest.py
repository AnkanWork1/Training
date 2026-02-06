import os
from pathlib import Path
import numpy as np
import joblib
import faiss
from tqdm import tqdm

from embeddings.clip_embedder import CLIPEmbedder


ROOT = Path(__file__).resolve().parents[1]

IMAGE_ROOT = ROOT / "data" / "raw" / "archive(1)" / "EnterpriseRAG_2025_02_markdown"

VECTOR_DIR = ROOT / "vectorstore" / "image"
INDEX_PATH = VECTOR_DIR / "index.faiss"
META_PATH = VECTOR_DIR / "meta.pkl"


def find_images(root: Path):
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = []

    for p in root.rglob("*"):
        if p.suffix.lower() in exts:
            images.append(p)

    return images


def main():

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    print("Scanning images in:", IMAGE_ROOT)

    images = find_images(IMAGE_ROOT)

    print("Found images:", len(images))

    if len(images) == 0:
        print("No images found.")
        return

    embedder = CLIPEmbedder()

    all_embeddings = []
    metas = []

    for img_path in tqdm(images):
        try:
            emb = embedder.embed_image(str(img_path))
        except Exception as e:
            print("Skipping:", img_path, "->", e)
            continue

        all_embeddings.append(emb)

        metas.append({
            "image_path": str(img_path),
            "file": img_path.name,
            "parent_dir": str(img_path.parent)
        })

    if not all_embeddings:
        print("No embeddings created.")
        return

    X = np.vstack(all_embeddings).astype("float32")

    print("Embedding matrix shape:", X.shape)

    dim = X.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(X)

    faiss.write_index(index, str(INDEX_PATH))
    joblib.dump(metas, META_PATH)

    print("Saved image index to:", INDEX_PATH)
    print("Saved image metadata to:", META_PATH)


if __name__ == "__main__":
    main()
