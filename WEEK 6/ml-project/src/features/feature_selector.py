# /features/feature_selector.py
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
import os

def feature_selector(X_train, X_test, y_train, n_features=10, save_path="features/feature_list.json"):
    """
    Performs feature selection and saves selected features.
    Returns reduced X_train, X_test and selected features list.
    """
    X_train_fs = X_train.copy()
    
    # 1️⃣ Remove highly correlated features
    corr_matrix = X_train_fs.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    drop_cols = [col for col in upper.columns if any(upper[col] > 0.9)]
    if drop_cols:
        print(f"Dropping highly correlated features: {drop_cols}")
    X_train_fs = X_train_fs.drop(columns=drop_cols)
    X_test_fs = X_test.drop(columns=drop_cols)
    
    # 2️⃣ Mutual Information (for info only)
    mi = mutual_info_regression(X_train_fs, y_train)
    mi_series = pd.Series(mi, index=X_train_fs.columns).sort_values(ascending=False)
    print("\nMutual Information Scores:")
    print(mi_series)
    
    # 3️⃣ RFE with RandomForest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    rfe = RFE(model, n_features_to_select=min(n_features, X_train_fs.shape[1]))
    rfe.fit(X_train_fs, y_train)
    
    selected_features = X_train_fs.columns[rfe.support_].tolist()
    print(f"\nSelected features via RFE ({len(selected_features)}): {selected_features}")
    
    # Reduce datasets
    X_train_final = X_train_fs[selected_features]
    X_test_final = X_test_fs[selected_features]
    
    # 4️⃣ Save selected features to JSON
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(selected_features, f, indent=4)
    
    # 5️⃣ Plot feature importance from RandomForest
    model.fit(X_train_final, y_train)
    importances = pd.Series(model.feature_importances_, index=selected_features)
    importances.sort_values().plot(kind="barh", figsize=(8,6), title="Feature Importances")
    plt.tight_layout()
    plt.show()
    
    return X_train_final, X_test_final, selected_features
