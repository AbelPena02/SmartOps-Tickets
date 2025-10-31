import logging

logger = logging.getLogger(__name__)

class PriorityScorer:
    def score(self, text: str) -> str:
        if not text:
            logger.warning("Priority scoring fallback: empty text")
            return "low"

        text_lower = text.lower()

        high_keywords = [
            "outage", "down", "unavailable", "critical",
            "security", "breach", "data loss", "incident",
            "production", "failure", "crash"
        ]

        medium_keywords = [
            "slow", "delay", "issue", "warning",
            "performance", "bug", "error"
        ]

        if any(word in text_lower for word in high_keywords):
            logger.info(f"Priority scored as HIGH based on text: {text}")
            return "high"

        if any(word in text_lower for word in medium_keywords):
            logger.info(f"Priority scored as MEDIUM based on text: {text}")
            return "medium"

        logger.info(f"Priority scored as LOW (no critical words found) for text: {text}")
        return "low"
