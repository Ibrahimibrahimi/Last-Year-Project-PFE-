"""
Review Sentiment Classifier
=============================
Wraps a pretrained sentiment model that exposes a .classify() method.
Returns 1 for positive sentiment, 0 for negative.

Usage:
    from ML.review_classifier import classifier
    label = classifier.classify("This lesson was great!")  # 1 or 0
"""

import os


class _ReviewClassifier:
    """
    Wrapper around the pretrained sentiment model.
    The actual model is expected to live at model.pkl in this directory.
    Exposes: classifier.classify(text) -> int (1=positive, 0=negative)
    """

    def __init__(self):
        self._model = None
        self._load()

    def _load(self):
        model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
        if os.path.exists(model_path):
            try:
                import pickle
                with open(model_path, "rb") as f:
                    self._model = pickle.load(f)
            except Exception as e:
                print(f"[review_classifier] Could not load model.pkl: {e}")
                self._model = None
        else:
            # Model file not present — use a simple heuristic as fallback
            self._model = None

    def classify(self, text: str) -> int:
        """
        Classify a review text.
        Returns 1 (positive) or 0 (negative).
        """
        if self._model is not None and hasattr(self._model, "classify"):
            return int(self._model.classify(text))

        # Fallback heuristic when pretrained model is unavailable
        negative_words = {
            "bad", "poor", "terrible", "awful", "boring", "useless",
            "confusing", "hard to understand", "waste", "worst", "hate",
            "horrible", "disappointing", "unclear", "wrong",
        }
        text_lower = text.lower()
        for word in negative_words:
            if word in text_lower:
                return 0
        return 1


# Singleton instance — import and use directly
classifier = _ReviewClassifier()

__all__ = ["classifier"]
