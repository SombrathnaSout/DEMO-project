if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import sqlite3
import pandas as pd

@data_exporter
def export_data(df, *args, **kwargs):
    if df.empty:
        print("No new data to export. The DataFrame is empty.")
        return

    # Get the new database path
    db_path = 'new_database.db'

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create the table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pos_table (
        transaction_id TEXT PRIMARY KEY,
        product_id TEXT,
        customer_id TEXT,
        store_id TEXT,
        quantity INTEGER,
        price REAL,
        transaction_date TEXT
    )
    """)
    conn.commit()

    # Read the existing transaction IDs from the database
    existing_transactions = pd.read_sql_query("SELECT transaction_id FROM pos_table", conn)
    
    # Find duplicates within the new data
    duplicate_transaction_ids = df['transaction_id'].isin(existing_transactions['transaction_id'])
    
    # Log duplicate information if found
    if duplicate_transaction_ids.any():
        print("Duplicate transactions found in new data:")
        print(df[duplicate_transaction_ids])
    
    # Remove duplicates from the new data
    df_to_insert = df[~duplicate_transaction_ids]
    
    # Write the dataframe to the database
    if not df_to_insert.empty:
        df_to_insert.to_sql('pos_table', conn, if_exists='append', index=False)
    else:
        print("No new data to insert after removing duplicates.")

    # Close the connection
    conn.close()

    print(f"Data exported to SQLite database: {db_path}")