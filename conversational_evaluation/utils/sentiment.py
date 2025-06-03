from transformers import pipeline
from typing import List, Dict


class SentimentAnalyzer:
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.pipeline = pipeline("sentiment-analysis", model=model_name)

    def score(self, texts: List[str]):
        return self.pipeline(texts)