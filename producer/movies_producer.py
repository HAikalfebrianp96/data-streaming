import json
import time
import os
import pandas as pd
from confluent_kafka import Producer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC = os.getenv("KAFKA_TOPIC", "streaming-movies")

producer = Producer({"bootstrap.servers": BOOTSTRAP})

files = {
    "netflix": "/app/dataset/netflix_titles.csv",
    "disney": "/app/dataset/disney_plus_titles.csv",
    "amazon": "/app/dataset/amazon_prime_titles.csv"
}

def delivery_report(err, msg):
    if err:
        print("❌ Delivery failed:", err)

for platform, path in files.items():
    df = pd.read_csv(path)
    df["platform"] = platform

    for _, row in df.iterrows():
        producer.produce(
            topic=TOPIC,
            value=json.dumps(row.to_dict()),
            callback=delivery_report
        )
        producer.poll(0)
        time.sleep(0.005)

producer.flush()
print("✅ Data sent to Kafka")
