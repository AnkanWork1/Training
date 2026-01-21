# src/pipelines/data_pipeline.py

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from src.utils.logger import logger  # your logger script

# Paths
RAW_PATH = "data/raw/dataset.csv"
PROCESSED_PATH = "data/processed/final.csv"
EDA_PATH = "data/processed/eda_report"
os.makedirs(EDA_PATH, exist_ok=True)

def load_data(path=RAW_PATH):
    logger.info(f"Loading raw data from {path}")
    df = pd.read_csv(path)
    logger.info(f"Data loaded with shape: {df.shape}")
    return df

def clean_data(df):
    logger.info("Starting cleaning process...")

    # Drop duplicates
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        df = df.drop_duplicates()
        logger.info(f"Dropped {dup_count} duplicate rows")

    # Handle missing numeric values with median
    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        missing = df[col].isnull().sum()
        if missing > 0:
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            logger.info(f"Filled {missing} missing values in {col} with median {median_val}")

    # Outlier removal using IQR
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        before = df.shape[0]
        df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]
        after = df.shape[0]
        if before != after:
            logger.info(f"Removed {before - after} outliers from {col} using IQR")

    logger.info("Data cleaning completed")
    return df

def save_data(df, path=PROCESSED_PATH):
    df.to_csv(path, index=False)
    logger.info(f"Processed data saved to {path}")

def generate_eda_report(df):
    logger.info("Generating EDA report...")
    
    # Correlation heatmap
    numeric_df = df.select_dtypes(include='number')
    plt.figure(figsize=(10,8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.savefig(f"{EDA_PATH}/correlation_heatmap.png")
    plt.close()

    # Missing values heatmap
    plt.figure(figsize=(10,6))
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Missing Values Heatmap")
    plt.savefig(f"{EDA_PATH}/missing_values_heatmap.png")
    plt.close()

    # Numeric feature distributions
    numeric_df.hist(figsize=(12,10))
    plt.tight_layout()
    plt.savefig(f"{EDA_PATH}/feature_distributions.png")
    plt.close()

    logger.info(f"EDA report saved in {EDA_PATH}")

def main():
    df = load_data()
    df_clean = clean_data(df)
    save_data(df_clean)
    generate_eda_report(df_clean)
    logger.info("Data pipeline completed successfully!")

if __name__ == "__main__":
    main()
