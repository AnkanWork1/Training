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

- 
    "LinearRegression": 
      1.  "MAE": 2328.798095605557,
      2.  "RMSE": 3067.221093422765,
      3.  "R2": 0.7983473703560606,
      4.  "CV_R2_mean": 0.7986179814507393
- 
    "RandomForest": 
      1.  "MAE": 1493.1289372502204,
      2.  "RMSE": 2086.6820379804763,
      3.  "R2": 0.9066689222885527,
      4.  "CV_R2_mean": 0.8869856422004686
- 
    "XGBoost"
      1.  "MAE": 1540.0905467511232,
      2.  "RMSE": 2122.2275857877817,
      3.  "R2": 0.9034621469318229,
      4.  "CV_R2_mean": 0.885637432836569
- 
    "NeuralNetwork"
      1.  "MAE": 2687.222102957572,
      2.  "RMSE": 3460.6597102821706,
      3.  "R2": 0.7432966601969337,
      4.  "CV_R2_mean": 0.7075566808381322


## 5. Best Model
- **Model**: RandomForest
- **R² Score**: 0.9066689222885527

Saved as:
/models/best_model.pkl


## 6. Saved Artifacts
- All trained models saved in `/models/`
- Metrics stored in:


/evaluation/metrics.json

## 7. Conclusion
RandomForest achieved the best generalization performance and was selected as the final production model.
