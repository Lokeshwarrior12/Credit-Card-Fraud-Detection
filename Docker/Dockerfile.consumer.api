FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer_predictor.py model.joblib ./
CMD ["python", "consumer_predictor.py"]
