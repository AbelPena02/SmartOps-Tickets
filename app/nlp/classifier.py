from joblib import load
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

MODEL_PATH = Path("app/nlp/models/ticket_classifier.joblib")

class TicketClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.rule_based = True
        self._load_model()

    def _load_model(self):
        """Try loading trained model, fallback to rule-based."""
        if MODEL_PATH.exists():
            try:
                logger.info("Loading trained Scikit-learn model...")
                data = load(MODEL_PATH)
                self.model = data.get("model")
                self.vectorizer = data.get("vectorizer")

                if self.model and self.vectorizer:
                    self.rule_based = False
                    logger.info("Model loaded successfully. AI mode enabled.")
                else:
                    logger.warning("Model file found but invalid. Using rule-based classification.")
            except Exception as e:
                logger.error(f"Error loading classifier model: {e}")
                self.rule_based = True
        else:
            logger.info("No trained model found. Using rule-based classification.")

    def classify(self, text: str) -> str:
        """Predict ticket category (model or rule-based)."""
        if not text:
            logger.warning("Classification fallback: empty text")
            return "unknown"

        text_lower = text.lower()

        if not self.rule_based and self.model and self.vectorizer:
            try:
                X = self.vectorizer.transform([text])
                prediction = self.model.predict(X)[0]
                logger.info(f"AI classification: '{prediction}' for text: {text}")
                return prediction
            except Exception as e:
                logger.error(f"Error in AI classification: {e}")

        logger.info(f"Rule-based classification used for text: {text}")

        if any(word in text_lower for word in ["error", "crash", "fail", "bug"]):
            return "bug"
        elif any(word in text_lower for word in ["add", "feature", "improve", "enhancement"]):
            return "feature"
        elif any(word in text_lower for word in ["bill", "payment", "invoice"]):
            return "billing"
        elif any(word in text_lower for word in ["help", "support", "password", "login"]):
            return "technical_support"
        elif any(word in text_lower for word in ["server", "network", "outage", "down"]):
            return "infrastructure"
        else:
            return "general"
