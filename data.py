from faker import Faker
import pandas as pd
import random
import uuid

fake = Faker()

def introduce_imperfections(record):
    if random.random() < 0.1:  # Introduce imperfections in 10% of the records
        field = random.choice(list(record.keys()))
        if field == "transaction_date":
            record[field] = "invalid_date"
        elif field in ["quantity", "price"]:
            record[field] = -1
        else:
            record[field] = ""
    return record

def generate_pos_transactions(num_records):
    data = []
    for _ in range(num_records):
        record = {
            "transaction_id": str(uuid.uuid4()),
            "product_id": str(uuid.uuid4()),
            "customer_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "quantity": random.randint(1, 100),
            "price": round(random.uniform(5.0, 100.0), 2),
            "transaction_date": fake.date_this_year().strftime("%Y-%m-%d"),
        }
        record = introduce_imperfections(record)
        data.append(record)
    return pd.DataFrame(data)

if __name__ == "__main__":
    pos_transactions = generate_pos_transactions(100)
    pos_transactions.to_csv("Datasets/pos_transactions.csv", index=False)
