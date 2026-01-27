# MODEL COMPARISON — REGRESSION

## 1. Objective
Train multiple regression models, compare performance, and automatically select the best model.

## 2. Models Trained
Implemented in `/training/train.py`:

1. Linear Regression
2. Random Forest Regressor
3. XGBoost Regressor
4. Neural Network (MLPRegressor)

## 3. Evaluation Strategy
- Train/Test split: 80/20
- Metrics used:
  - MAE (Mean Absolute Error)
  - RMSE (Root Mean Squared Error)
  - R² Score

> Note: Classification metrics (Accuracy, Precision, Recall, F1, ROC-AUC) are **not applicable** since this is a regression task.

## 4. Model Performance

| Model | MAE | RMSE | R² |
|------|-----|------|----|
| Linear Regression | 2743.06 | 3611.66 | 0.720 |
| Random Forest | 2251.63 | 3081.88 | 0.796 |
| **XGBoost** | **2218.36** | **3028.44** | **0.803** |
| Neural Network | 4113.49 | 5200.35 | 0.420 |

## 5. Best Model
- **Model**: XGBoost Regressor
- **R² Score**: 0.8034

Saved as:
/models/best_model.pkl


## 6. Saved Artifacts
- All trained models saved in `/models/`
- Metrics stored in:


/evaluation/metrics.json

## 7. Conclusion
XGBoost achieved the best generalization performance and was selected as the final production model.
