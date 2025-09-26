# src/producer.py

import pandas as pd
from kafka import KafkaProducer
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv(DATA_DIR / "creditcard_processed.csv")

print("Starting to send transaction data...")

for index, row in df.iterrows():
    message = row.to_dict()

    # --- THIS IS THE FIX ---
    # We ensure all keys are in the correct case that the Pydantic model expects.
    # This converts keys like 'v1', 'v2' to 'V1', 'V2'.
    corrected_message = {k.upper() if k.startswith('v') else k: v for k, v in message.items()}
    # --------------------

    producer.send('transactions', value=corrected_message)

    print(f"Sent transaction #{index}")
    time.sleep(0.01)

producer.flush()
print("All transaction data sent successfully.")