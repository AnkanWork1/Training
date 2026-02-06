import torch
import numpy as np
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


class CLIPEmbedder:

    def __init__(self, model_name="openai/clip-vit-base-patch32", device=None):

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device

        self.model = CLIPModel.from_pretrained(model_name).to(self.device)

        self.processor = CLIPProcessor.from_pretrained(
            model_name,
            use_fast=False
        )

        self.model.eval()

    def _unwrap_features(self, out):
        """
        Make this robust across transformers versions.
        """
        if isinstance(out, torch.Tensor):
            return out

        # Newer / different builds may return a model output
        if hasattr(out, "text_embeds"):
            return out.text_embeds

        if hasattr(out, "image_embeds"):
            return out.image_embeds

        if hasattr(out, "pooler_output"):
            return out.pooler_output

        raise RuntimeError(f"Unknown CLIP output type: {type(out)}")

    @torch.no_grad()
    def embed_image(self, image_path: str) -> np.ndarray:

        image = Image.open(image_path).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        ).to(self.device)

        out = self.model.get_image_features(**inputs)
        features = self._unwrap_features(out)

        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].astype("float32")

    @torch.no_grad()
    def embed_text(self, text: str) -> np.ndarray:

        inputs = self.processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(self.device)

        out = self.model.get_text_features(**inputs)
        features = self._unwrap_features(out)

        features = features / features.norm(dim=-1, keepdim=True)

        return features.cpu().numpy()[0].astype("float32")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--image", type=str, help="Path to image")
    parser.add_argument("--text", type=str, help="Text query")
    args = parser.parse_args()

    if not args.image and not args.text:
        print("Provide at least one of --image or --text")
        raise SystemExit(1)

    embedder = CLIPEmbedder()

    if args.image:
        emb = embedder.embed_image(args.image)
        print("Image embedding shape:", emb.shape)

    if args.text:
        emb = embedder.embed_text(args.text)
        print("Text embedding shape:", emb.shape)
