import argparse
import os
import numpy as np
import faiss
import pickle
from pipelines.image_ocr_blip import MultimodalEmbedder

INDEX_PATH = "vectorstore/multimodal/index.faiss"
META_PATH = "vectorstore/multimodal/meta.pkl"

def main(image_folder):
    print("Looking for images in:", image_folder)
    os.makedirs("vectorstore/multimodal", exist_ok=True)

    embedder = MultimodalEmbedder()

    # find images
    image_files = [
        os.path.join(dp, f)
        for dp, dn, filenames in os.walk(image_folder)
        for f in filenames
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]


    if not image_files:
        print("No images found in folder!")
        return

    embeddings = []
    metadata = []

    for img_path in image_files:
        try:
            print("Processing:", img_path)
            ocr_text = embedder.extract_ocr_text(img_path)
            caption = embedder.generate_caption(img_path)
            combined_text = (ocr_text + " " + caption).strip()
            text_emb = embedder.embed_text(combined_text)
            embeddings.append(text_emb)

            metadata.append({
                "image_path": img_path,
                "ocr_text": ocr_text,
                "caption": caption
            })
        except Exception as e:
            print("Error processing", img_path, e)

    embeddings = np.array(embeddings).astype("float32")
    if len(embeddings) == 0:
        print("No embeddings generated!")
        return

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Saved multimodal index to: {INDEX_PATH}")
    print(f"Saved metadata to: {META_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image_folder", type=str, required=True, help="Path to folder containing images"
    )
    args = parser.parse_args()
    main(args.image_folder)
