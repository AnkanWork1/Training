# src/training/tuning2.py

import json
from pathlib import Path
import joblib
import optuna
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score

BASE_DIR = Path(__file__).parent.parent
best_model_path = BASE_DIR / "models/best_model.pkl"

# Load previously trained best model
best_model = joblib.load(best_model_path)

MODELS_DIR = BASE_DIR / "models"
TUNING_DIR = BASE_DIR / "tuning"
MODELS_DIR.mkdir(exist_ok=True, parents=True)
TUNING_DIR.mkdir(exist_ok=True, parents=True)

def tune_xgboost_optuna(X_train, y_train, n_trials=30):
    """
    Hyperparameter tuning for XGBoost using Optuna
    """
    def objective(trial):
        # Define hyperparameter search space
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 300),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0)
        }

        model = XGBRegressor(**params, random_state=42, verbosity=0)
        score = cross_val_score(model, X_train, y_train, cv=5, scoring="r2").mean()
        return score  # Optuna maximizes this

    # Create study and optimize
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    # Train best model on full training set
    best_params = study.best_params
    tuned_model = XGBRegressor(**best_params, random_state=42, verbosity=0)
    tuned_model.fit(X_train, y_train)

    # Save tuned model
    joblib.dump(tuned_model, MODELS_DIR / "xgb_tuned_optuna.pkl")

    # Save tuning results
    results = {
        "best_params": best_params,
        "best_cv_r2": study.best_value
    }
    with open(TUNING_DIR / "results_optuna.json", "w") as f:
        json.dump(results, f, indent=4)

    print("✅ Optuna hyperparameter tuning completed!")
    print("Best parameters:", best_params)
    print(f"Best CV R2: {study.best_value:.4f}")

    return tuned_model, results
