# -----------------------------
# 0️⃣ Imports
# -----------------------------
import pandas as pd
import joblib
import json
from pathlib import Path

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Model training functions
from models.train_models import (
    train_linear_regression,
    train_random_forest,
    train_xgboost,
    train_neural_network
)

# -----------------------------
# 1️⃣ Training function
# -----------------------------
def train_all_models(X_train, X_test, y_train, y_test):
    """
    Trains multiple regression models, evaluates them, 
    saves all models and the best model, and returns metrics.
    """
    # Train models
    models = {
        "LinearRegression": train_linear_regression(X_train, y_train),
        "RandomForest": train_random_forest(X_train, y_train),
        "XGBoost": train_xgboost(X_train, y_train),
        "NeuralNetwork": train_neural_network(X_train, y_train)
    }

    # Evaluate models
    metrics = {}
    best_model_name = None
    best_r2 = -float('inf')
    best_model_obj = None

    for name, model in models.items():
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5

        r2 = r2_score(y_test, y_pred)

        metrics[name] = {"MAE": mae, "RMSE": rmse, "R2": r2}

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model_obj = model
    
    # -----------------------------
    # Save models and metrics safely
    # -----------------------------
    # BASE_DIR = folder where this train.py exists
    BASE_DIR = Path(__file__).parent.parent  # go up from training/ to src/
    
    MODELS_DIR = BASE_DIR / "models"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    EVAL_DIR = BASE_DIR / "evaluation"
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save all models
    for name, model in models.items():
        joblib.dump(model, MODELS_DIR / f"{name}.pkl")
    
    # Save best model
    joblib.dump(best_model_obj, MODELS_DIR / "best_model.pkl")
    

    # Save metrics
    with open(EVAL_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Best model: {best_model_name} with R2={best_r2:.4f}")
    print("All models and metrics saved.")

    return models, best_model_obj, metrics

# -----------------------------
# 2️⃣ Optional: Example of usage if running this script directly
# -----------------------------
if __name__ == "__main__":
    # Load preprocessed data
    DATA_DIR = Path("../data/processed")
    X_train = pd.read_csv(DATA_DIR / "X_train_final.csv")
    X_test  = pd.read_csv(DATA_DIR / "X_test_final.csv")
    y_train = pd.read_csv(DATA_DIR / "y_train.csv").squeeze()
    y_test  = pd.read_csv(DATA_DIR / "y_test.csv").squeeze()

    # Call the training function
    train_all_models(X_train, X_test, y_train, y_test)
