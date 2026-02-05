def build_context(metadata, selected_ids):

    blocks = []

    for rank, idx in enumerate(selected_ids, 1):

        m = metadata[idx]

        block = {
            "rank": rank,
            "text": m["text"],
            "source_pdf": m.get("source_pdf"),
            "images": m.get("image_paths", []),
            "chunk_id": m.get("chunk_id", idx)
        }

        blocks.append(block)

    return blocks
