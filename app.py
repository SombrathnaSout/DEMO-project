from flask import Flask, jsonify
from faker import Faker
import random
import uuid

app = Flask(__name__)
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
    return data

@app.route("/generate", methods=["GET"])
def generate_data():
    num_records = 10  # generate 10 records
    data = generate_pos_transactions(num_records)
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
