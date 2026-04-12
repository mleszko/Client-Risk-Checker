import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("training_data.csv")
df["text"] = df["industry"] + " " + df["description"]

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["text"])
y = df["label"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/vectorizer.pkl")
joblib.dump(model, "models/risk_classifier.pkl")

print("✅ Model and vectorizer saved.")
