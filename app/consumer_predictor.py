import json
import joblib
import time
from kafka import KafkaConsumer, KafkaProducer
from prometheus_client import start_http_server, Counter, Histogram, Gauge
import numpy as np


Kafka_bootstrap = "localhost:9092"
Consume_topic = "transactions"
Publish_topic = "predictions"
Model_path = "model.joblib"
Metrics_port = 8001

processed = Counter("transcations_processed_total", "Total transactions processed")
fraud_pred = Counter("predicited_fraud_total", "Total predication frauds")
processing_time = Histogram("transaction_processing_seconds", "Time to score a transactions")
last_score = Gauge("last_prediction_score", "Score for last prediction")


def load_model(path=Model_path):
    return joblib.load(path)

FEATURES = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10",
            "v11","v12","v13","v14","v15","v16","v17","v18","v19",
            "v20","v21","v22","v23","v24","v25","v26","v27","v28","Amount"]

def extract_features(tx_json):
    X = [tx_json.get(f, 0) for f in FEATURES]  # fill missing with 0
    return np.array(X, dtype=float).reshape(1, -1)

def main():
    model = load_model()
    start_http_server(Metrics_port)
    consumer = KafkaConsumer(
        Consume_topic,
        bootstrap_servers = Kafka_bootstrap,
        value_deserializer = lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset = "earliest",
        enable_auto_commit = True,
        group_id = "predictor-group"
    )
    producer = KafkaProducer(
        bootstrap_servers=Kafka_bootstrap,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    try:
        for msg in consumer:
            tx = msg.value
            t0 = time.time()
            try:
                X = extract_features(tx)
                print("Feature shape:", X.shape)
                score = model.predict_proba(X)[:,1][0]
                label = int(score >= 0.5)
            except Exception as e:
                print("Error", e)
                continue

            dt = time.time() - t0
            processed.inc()
            processing_time.observe(dt)
            last_score.set(score)
            if label == 1:
                fraud_pred.inc()

            result = {
                "transaction": tx,
                "score": float(score),
                "label": label,
                "processing_time": dt,
                "timestamp": time.time()
            }
            producer.send(Publish_topic, result)

    except KeyboardInterrupt:
        print("Consumer stopped manually.")
    finally:
        producer.flush()
        consumer.close()
        producer.close()
        print("Kafka connections closed.")



if __name__ == "__main__":
    main()