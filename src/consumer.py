# src/consumer.py

from kafka import KafkaConsumer
import json
import requests

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='fraud-detector-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

API_ENDPOINT = "http://127.0.0.1:8000/predict"

print("Consumer is listening for transactions...")

for message in consumer:
    transaction = message.value

    if 'Class' in transaction:
        del transaction['Class']

    print(f"\nReceived transaction with V1 value: {transaction['V1']}")

    # --- ADD THIS DEBUG LINE ---
    print(f"DEBUG: Sending this data to API -> {transaction}")
    # -------------------------

    try:
        response = requests.post(API_ENDPOINT, json=transaction)
        response.raise_for_status()

        prediction = response.json()

        if prediction.get("is_fraud") == 1:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"!!! FRAUD ALERT DETECTED !!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            print("Transaction is legitimate.")

    except requests.exceptions.RequestException as e:
        print(f"Could not connect to the API: {e}")