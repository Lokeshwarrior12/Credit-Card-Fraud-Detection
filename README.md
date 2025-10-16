# Credit-Card-Fraud-Detection
## Real-Time Credit Card Fraud Detection (Sample Project)

## Project Overview
This is a **small sample project** that simulates a real-time credit card fraud detection system.  
It demonstrates an **end-to-end ML workflow**, including:

- Streaming transactions (Kafka)
- Fraud prediction (XGBoost)
- API exposure (FastAPI)
- Optional experiment tracking (MLflow)
- Optional containerization (Docker/Kubernetes)

**Objective:** Detect fraudulent credit card transactions in real-time.

---

## Tech Stack

- Python 3.10+
- scikit-learn / XGBoost
- Apache Kafka (3.x recommended for Windows)
- FastAPI
- Docker + Kubernetes (Minikube, optional)
- MLflow (optional, experiment tracking)

---

## Project Structure

creditcard_fraud_sample/
 data/
└─ creditcard.csv # Kaggle dataset (not included)
 app/
 ├─ producer.py # Kafka producer
 ├─ consumer.py # Kafka consumer + ML prediction
 └─ main.py # FastAPI API
 Dockerfile # Optional containerization
 requirements.txt
README.md
.gitignore


---

## Setup Instructions

### 1️⃣ Install Python dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
CMD
pip install -r requirements.txt

pandas
numpy
scikit-learn
xgboost
fastapi
uvicorn
kafka-python
mlflow
joblib


2️⃣ Kafka Setup (Local)

1.Download Kafka 3.x for Windows: Kafka Downloads
2.Extract to a short path (e.g., C:\kafka) to avoid Windows path issues
3.Start ZooKeeper (CMD 1):
cd C:\kafka\bin\windows
zookeeper-server-start.bat ..\..\config\zookeeper.properties
4.Start Kafka server (CMD 2):
kafka-server-start.bat ..\..\config\server.properties

5.Create Kafka topic transactions (CMD 3):
kafka-topics.bat --create --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

3️⃣ Prepare Dataset
Download the Kaggle Credit Card Fraud Dataset and place it in "data/creditcard.csv". Create a folder data in project.

4️⃣ Train the ML Model
Run a training script or include this in your consumer/API script:
CMD
python train_xgb.py

5️⃣ Run Kafka Producer & Consumer
Producer (send transactions to Kafka):
CMD
python app/producer.py
Consumer (read transactions + predict fraud):
CMD
python app/consumer.py
Sample Consumer Output:
Transaction: 12345, Fraud: 0
Transaction: 12346, Fraud: 1
Transaction: 12347, Fraud: 0

6️⃣ Run FastAPI API
CMD
uvicorn app.main:app --host 0.0.0.0 --port 8000
Test API:
CMD
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"V1":0.1,"V2":0.2,"Amount":100,...}'

7️⃣ Optional: MLflow Experiment Tracking
import mlflow
import mlflow.xgboost

with mlflow.start_run():
    model.fit(X_train_scaled, y_train)
    mlflow.log_param("model", "xgboost")
    mlflow.log_metric("accuracy", model.score(X_test_scaled, y_test))
    mlflow.xgboost.log_model(model, "model")
Start MLflow UI:
CMD
mlflow ui

8️⃣ Optional: Docker / Kubernetes
Dockerfile:

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD
Build: docker build -t fraud-api .
CMD
Run: docker run -p 8000:8000 fraud-api
Deploy to Minikube if desired

# 9. Docker
Docker allows you to package your project and its dependencies into a container, so it runs anywhere consistently.
Dockerfile (already included):

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


Build Docker Image:
CMD
docker build -t fraud-api .
Run Docker Container:
CMD
docker run -p 8000:8000 fraud-api

The FastAPI API is now accessible at http://localhost:8000/predict
You can use the same Kafka setup, or run Kafka inside another container for full isolation.

# 10. Kubernetes (Minikube)
Kubernetes (K8s) lets you orchestrate containers, scale them, and monitor their health. For local testing, Minikube is perfect.
Start Minikube:
minikube start
Create Deployment for FastAPI container:
Apply deployment:
CMD
kubectl apply -f deployment.yaml
Expose the service:
CMD
kubectl expose deployment fraud-api-deployment --type=NodePort --port=8000
Get the service URL:
CMD
minikube service fraud-api-deployment --url
This gives a URL where your FastAPI API is accessible inside the cluster.

# Conclusion
This project demonstrates a full end-to-end workflow for:
Streaming data ingestion (Kafka)
Fraud prediction (ML model)
API exposure (FastAPI)
Optional experiment tracking (MLflow)
Optional containerization (Docker/Kubernetes)

It’s a learning-focused prototype, scalable for more advanced implementations.
- Project overview  
- Dependencies  
- Kafka setup  
- ML training  
- Producer & consumer usage  
- FastAPI testing  
- Optional MLflow / Docker setup  
- Sample outputs  

