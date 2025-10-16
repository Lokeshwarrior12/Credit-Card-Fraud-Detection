[Offline Training] --(model artifact)--> MLflow
                                 |
                                 V
                        (export model file: model.joblib)
Kafka Topic: "transactions"  <-- Producer (simulated) pushes JSON txns
                                 |
                                 V
                         Predictor Consumer (K8s pod)
                         - loads model.joblib
                         - scores transactions
                         - pushes result to "predictions" topic OR stores results in DB
                         - exposes Prometheus metrics (throughput, latency, fraud_count)
                                 |
                                 V
                     FastAPI (optional) <--> For manual single prediction / admin
                                 |
                                 V
                      Prometheus scrapes /metrics endpoints
                                 |
                                 V
                         Grafana dashboard
