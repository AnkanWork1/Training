import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np


class CrossEncoderReranker:

    def __init__(self, model_name="BAAI/bge-reranker-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name
        ).to(self.device)

        self.model.eval()

    def rerank(self, query, passages):
        """
        passages : list[str]
        return    : list[float]
        """

        pairs = [(query, p) for p in passages]

        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            scores = self.model(**inputs).logits.squeeze(-1)

        return scores.cpu().numpy().tolist()
