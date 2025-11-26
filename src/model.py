import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def train_model(X, y, out_path="models/rf_model.joblib"):
    """
    Train a RandomForest model and save it to out_path.
    X: pandas DataFrame or 2D array of features
    y: pandas Series or 1D array of targets
    """
    model = RandomForestRegressor(n_estimators=150, random_state=42)
    model.fit(X, y)

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    joblib.dump(model, out_path)
    return model

def eval_model(model, X, y):
    """
    Return a small metrics dict for MAE and RMSE on provided X, y.
    """
    preds = model.predict(X)
    mae = mean_absolute_error(y, preds)
    rmse = np.sqrt(mean_squared_error(y, preds))
    return {"mae": mae, "rmse": rmse}
