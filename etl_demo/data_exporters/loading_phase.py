if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import sqlite3
import pandas as pd

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
        # Check for duplicate rows in the existing data
        duplicate_query = """
        SELECT *, COUNT(*) as count
        FROM transactions
        GROUP BY transaction_id, product_id, customer_id, store_id, quantity, price, transaction_date
        HAVING count > 1;
        """
        duplicates = pd.read_sql_query(duplicate_query, conn)
        if not duplicates.empty:
            print("Duplicate rows found:")
            print(duplicates)
        else:
            print("No duplicate rows found.")
        
        # Write the dataframe to the database
        df.to_sql('transactions', conn, if_exists='append', index=False)
    else:
        # If table doesn't exist, just create it
        df.to_sql('transactions', conn, if_exists='replace', index=False)

    # Close the connection
    conn.close()

    print(f"Data exported to SQLite database: {db_path}")