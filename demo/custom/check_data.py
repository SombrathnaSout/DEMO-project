if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
import pandas as pd

@custom
def view_data(df, *args, **kwargs):
    print("Data Information:")
    print(df.info())
    
    print("\nData Description:")
    print(df.describe(include='all'))
    
    print("\nSample Data:")
    print(df.head())

    print("\nNumber of rows:", len(df))
    print("Number of unique transaction IDs:", df['transaction_id'].nunique())
    print("Number of unique product IDs:", df['product_id'].nunique())
    print("Number of unique customer IDs:", df['customer_id'].nunique())
    print("Number of unique store IDs:", df['store_id'].nunique())

    print("\nColumns with missing values:")
    print(df.isnull().sum())
    
    print("\nData Preview:")
    print(df.head(10))
