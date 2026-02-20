import os
import torch
import pytesseract
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from transformers import BlipProcessor, BlipForConditionalGeneration
import numpy as np


class MultimodalEmbedder:
    def __init__(self, clip_model_name="openai/clip-vit-base-patch32", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # CLIP for embeddings
        self.clip_model = CLIPModel.from_pretrained(clip_model_name).to(self.device)
        self.clip_processor = CLIPProcessor.from_pretrained(clip_model_name)
        self.clip_model.eval()

        # BLIP for captions
        self.blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.blip_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).to(self.device)
        self.blip_model.eval()

    @torch.no_grad()
    def embed_text(self, text: str) -> np.ndarray:
        inputs = self.clip_processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=77
        ).to(self.device)

        output = self.clip_model.get_text_features(**inputs)

        # Ensure we get a tensor
        if not torch.is_tensor(output):
            # sometimes transformers return BaseModelOutputWithPooling
            features = output.pooler_output if hasattr(output, "pooler_output") else output.last_hidden_state.mean(dim=1)
        else:
            features = output

        # normalize
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()[0].astype("float32")

    @torch.no_grad()
    def embed_image(self, image_path: str) -> np.ndarray:
        image = Image.open(image_path).convert("RGB")
        inputs = self.clip_processor(images=image, return_tensors="pt").to(self.device)

        output = self.clip_model.get_image_features(**inputs)

        # Ensure we get a tensor
        if not torch.is_tensor(output):
            features = output.pooler_output if hasattr(output, "pooler_output") else output.last_hidden_state.mean(dim=1)
        else:
            features = output

        # normalize
        features = features / features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()[0].astype("float32")

    @torch.no_grad()
    def generate_caption(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.blip_processor(images=image, return_tensors="pt").to(self.device)
        output_ids = self.blip_model.generate(**inputs, max_new_tokens=50)
        caption = self.blip_processor.decode(output_ids[0], skip_special_tokens=True)
        return caption

    def extract_ocr_text(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        return pytesseract.image_to_string(image)
    
    def build_query_from_image(self, image_path: str) -> str:
        ocr = self.extract_ocr_text(image_path)
        caption = self.generate_caption(image_path)

        return (
            "OCR:\n" + ocr.strip() +
            "\n\nCAPTION:\n" + caption.strip()
        )

