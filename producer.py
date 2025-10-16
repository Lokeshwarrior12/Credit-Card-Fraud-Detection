import pandas as pd
import json
import time
from kafka import KafkaProducer

DATA_PATH = "data/creditcard.csv"
KAFKA_TOPIC = "transactions"
KAFKA_BOOTSTRAP = "localhost:9092"

def sample_transaction(df):
    """Randomly select one transaction."""
    return df.sample(1).iloc[0].to_dict()

def main(rate_per_sec=5):
    df = pd.read_csv(DATA_PATH)
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    print(f"✅ Kafka Producer connected to {KAFKA_BOOTSTRAP}, sending {rate_per_sec} tx/sec to topic '{KAFKA_TOPIC}'...")

    try:
        while True:
            tx = sample_transaction(df)
            tx["timestamp"] = time.time()
            producer.send(KAFKA_TOPIC, tx)
            print("Sent transaction:", tx.get("Time"))
            time.sleep(1.0 / rate_per_sec)
    except KeyboardInterrupt:
        print("\n🛑 Stopping producer...")
    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main(rate_per_sec=10)
