import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.features import load_data, featurize
from src.model import train_model, eval_model
import pandas as pd
import os

def main():
    
    courses, hist = load_data()
    print("Loaded:", len(courses), "courses; historical rows:", len(hist))

   
    X, y, courses_full = featurize(courses, hist)
    print("Feature matrix shape:", X.shape)

    model = train_model(X, y, out_path="models/rf_model.joblib")
    print("Model trained and saved to models/rf_model.joblib")

    
    metrics = eval_model(model, X, y)
    print("Training metrics:", metrics)

    preds = model.predict(X).round().astype(int)
    courses_full["predicted_students"] = preds
    out_csv = "data/synthetic/courses_with_predictions.csv"
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    courses_full.to_csv(out_csv, index=False)
    print("Saved predictions to:", out_csv)

if __name__ == "__main__":
    main()
