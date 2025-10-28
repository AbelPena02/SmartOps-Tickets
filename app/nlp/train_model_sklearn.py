import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from app.nlp.training_data import TRAINING_DATA

MODEL_DIR = "app/nlp/models"
MODEL_PATH = os.path.join(MODEL_DIR, "ticket_classifier.pkl")

def train_model():
    texts = [text for text, label in TRAINING_DATA]
    labels = [label for text, label in TRAINING_DATA]

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    model.fit(texts, labels)

    os.makedirs(MODEL_DIR, exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved at: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
