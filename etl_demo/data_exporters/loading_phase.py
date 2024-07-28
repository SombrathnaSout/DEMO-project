if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import sqlite3
import pandas as pd  # Import pandas if not already imported
from mage_ai.data_preparation.shared.secrets import get_secret_value

@data_exporter
def export_data(df, *args, **kwargs):
    # Get the database path from secrets
    db_path = 'database.db'

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Check for duplicates before writing the dataframe to the database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Read the existing data
        existing_df = pd.read_sql_query("SELECT * FROM transactions", conn)
        
        # Find the difference between the new dataframe and the existing one
        new_data = df[~df.apply(tuple, 1).isin(existing_df.apply(tuple, 1))]
    else:
        new_data = df
    
    # Write only the new data to the database
    if not new_data.empty:
        new_data.to_sql('transactions', conn, if_exists='append', index=False)

    # Close the connection
    conn.close()

    print(f"Data exported to SQLite database: {db_path}")

def test_output(df) -> None:
    db_path = 'database.db'
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Check if the table exists
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions';")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Read the data from the database
        existing_df = pd.read_sql_query("SELECT * FROM transactions", conn)
        
        # Check if the dataframes are identical
        data_exists = df.apply(tuple, 1).isin(existing_df.apply(tuple, 1)).all()
    else:
        data_exists = False
    
    # Close the connection
    conn.close()
    
    # Assert that the data does not exist in the database
    assert not data_exists, 'The same data is already in the database'
    
    # Assert that the dataframe is not empty
    assert df is not None, 'The output is undefined'
    assert len(df) > 0, 'The output is empty'
