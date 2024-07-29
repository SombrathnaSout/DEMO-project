if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(df, *args, **kwargs):
    # Data quality checks
    required_columns = ['transaction_id', 'quantity', 'price', 'transaction_date', 'customer_id','product_id','store_id']
    for col in required_columns:
        assert col in df.columns, f"Missing '{col}' column"

    # Replace invalid dates with a placeholder
    df['transaction_date'] = df['transaction_date'].apply(lambda x: x if x != 'invalid_date' and pd.notnull(x) else '0000-00-00')

    # Remove rows with negative or zero quantities and prices
    df = df[df['quantity'] > 0]
    df = df[df['price'] > 0]

    # Remove rows with excessively high quantities (assuming a max realistic value)
    df = df[df['quantity'] <= 1000]

    # Replace invalid customer_ids with a placeholder
    df['customer_id'] = df['customer_id'].apply(lambda x: x if pd.notnull(x) and x != '' else 'MISSING')
    df['store_id'] = df['store_id'].apply(lambda x: x if pd.notnull(x) and x != '' else 'MISSING')
    df['product_id'] = df['product_id'].apply(lambda x: x if pd.notnull(x) and x != '' else 'MISSING')
    # Remove duplicate transaction IDs within the incoming data
    df = df.drop_duplicates(subset=['transaction_id'])

    return df

@test
def test_output(df) -> None:
    assert df is not None, 'The output is undefined'
    assert len(df) > 0, 'The output is empty'
    assert (df['quantity'] > 0).all(), "Found non-positive quantities"
    assert (df['price'] > 0).all(), "Found non-positive prices"
    assert df['transaction_date'].str.match(r'^\d{4}-\d{2}-\d{2}$|^0000-00-00$').all(), "Found invalid dates"
    assert df['customer_id'].str.match(r'^[a-zA-Z0-9\-]+$|^MISSING$').all(), "Found invalid customer IDs"