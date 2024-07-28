if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(df, *args, **kwargs):
    # Data quality checks
    assert 'transaction_id' in df.columns, "Missing 'transaction_id' column"
    assert 'quantity' in df.columns, "Missing 'quantity' column"
    assert 'price' in df.columns, "Missing 'price' column"
    assert 'transaction_date' in df.columns, "Missing 'transaction_date' column"

    # Remove rows with invalid dates
    df = df.dropna(subset=['transaction_date'])

    # Remove rows with negative or zero quantity/price
    df = df[(df['quantity'] > 0) & (df['price'] > 0)]

    # Remove rows with quantity > 1000 (assuming this is an unrealistic value)
    df = df[df['quantity'] <= 1000]

    return df

@test
def test_output(df) -> None:
    assert df is not None, 'The output is undefined'
    assert len(df) > 0, 'The output is empty'
    assert (df['quantity'] > 0).all(), "Found non-positive quantities"
    assert (df['price'] > 0).all(), "Found non-positive prices"
    assert (df['quantity'] <= 1000).all(), "Found quantities exceeding 1000"