if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@data_loader
def load_data(*args, **kwargs):
    # Define the directory where your files are located
    data_dir = 'Datasets/pos_transactions.csv'
    
    # Load CSV file
    df = pd.read_csv(data_dir)
    return df

@test
def test_output(df) -> None:
    assert df is not None, 'The output is undefined'
    assert len(df) > 0, 'The output is empty'
    expected_columns = ['transaction_id', 'product_id', 'customer_id', 'store_id', 'quantity', 'price', 'transaction_date']
    assert all(col in df.columns for col in expected_columns), 'Missing expected columns'
