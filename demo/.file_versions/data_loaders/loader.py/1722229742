if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import requests

@data_loader
def load_data(*args, **kwargs):
    # Fetch data from the API
    response = requests.get('http://127.0.0.1:5000/generate')
    data = response.json()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

@test
def test_output(df) -> None:
    assert df is not None, 'The output is undefined'
    assert len(df) > 0, 'The output is empty'
    expected_columns = ['transaction_id', 'product_id', 'customer_id', 'store_id', 'quantity', 'price', 'transaction_date']
    assert all(col in df.columns for col in expected_columns), 'Missing expected columns'
