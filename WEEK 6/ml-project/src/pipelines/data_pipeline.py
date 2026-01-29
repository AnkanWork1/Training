# src/pipelines/data_pipeline.py

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from utils.logger import logger  # your logger script

# Paths
RAW_PATH = "data/raw/dataset.csv"
PROCESSED_PATH = "data/processed/final.csv"
EDA_PATH = "logs/data_pipeline.log"
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
