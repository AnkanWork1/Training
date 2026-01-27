# /features/feature_selector.py

import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression, RFE
from sklearn.linear_model import LinearRegression

def remove_highly_correlated_features(X, threshold=0.9):
    """
    Removes features that are highly correlated with others.
    """
    '''
    2. Why remove features based on correlation?
    Highly correlated features contain redundant information.
    If two features are almost perfectly correlated:
    Model can get confused
    Might give too much weight to similar information
    Can increase overfitting
    Slows down training
    Example:
    engineSize and tax could be strongly correlated (bigger engines → higher road tax).
    Keeping both doesn’t add much new information, so we can remove one.
    '''
    corr_matrix = X.corr().abs()
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
    X_reduced = X.drop(columns=to_drop)
    
    print(f"Dropped due to correlation > {threshold}: {to_drop}")
    return X_reduced, to_drop

    
def select_features_mutual_info(X, y, top_k=None):
    mi_scores = mutual_info_regression(X, y, random_state=42)
    mi_df = pd.DataFrame({
        "feature": X.columns,
        "mi_score": mi_scores
    }).sort_values(by="mi_score", ascending=False)

    if top_k:
        selected_features = mi_df.head(top_k)["feature"].tolist()
    else:
        selected_features = mi_df[mi_df["mi_score"] > 0.01]["feature"].tolist()

    return selected_features, mi_df


def select_features_rfe(X, y, n_features=5):
    """
    Select features using Recursive Feature Elimination (RFE) with LinearRegression.
    """
    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=n_features)
    rfe.fit(X, y)
    
    selected_features = X.columns[rfe.support_]
    return selected_features

def run_feature_selection(X, y, corr_threshold=0.9, top_k_mi=None, n_rfe=5):
    """
    Full pipeline: correlation threshold → mutual info → RFE
    """
    # 1️⃣ Remove highly correlated features
    X_corr, dropped_corr = remove_highly_correlated_features(X, threshold=corr_threshold)
    
    # 2️⃣ Select with mutual information
    X_mi, selected_mi, mi_df = select_features_mutual_info(X_corr, y, top_k=top_k_mi)
    
    # 3️⃣ Select final features with RFE
    X_final, selected_rfe = select_features_rfe(X_mi, y, n_features=n_rfe)
    
    return X_final, selected_rfe, mi_df, dropped_corr
