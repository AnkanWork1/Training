# src/training/tuning.py
import json
from pathlib import Path
import joblib
from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
TUNING_DIR = BASE_DIR / "evaluation/tuning"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
TUNING_DIR.mkdir(parents=True, exist_ok=True)


def tune_xgboost(X_train, y_train):
    """
    Tune XGBoost hyperparameters using GridSearchCV
    """
    # Hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1]
    }

    xgb = XGBRegressor(random_state=42, verbosity=0)

    grid_search = GridSearchCV(
        estimator=xgb,
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    # Save tuned model
    joblib.dump(best_model, MODELS_DIR / "xgb_tuned.pkl")

    # Save tuning results
    results = {
        "best_params": best_params,
        "best_cv_r2": best_score
    }

    with open(TUNING_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("✅ Hyperparameter tuning completed!")
    print("Best parameters:", best_params)
    print(f"Best CV R2: {best_score:.4f}")

    return best_model, results
