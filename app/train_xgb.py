# train_xgb.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
import xgboost as xgb
import joblib
import mlflow
import mlflow.sklearn

DATA_PATH = "data/creditcard.csv"  # download from Kaggle into data/

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    X = df.drop(columns=["Class", "Time"])  # Time often dropped
    y = df["Class"]
    return X, y

def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
    mlflow.set_experiment("creditcard-fraud")
    with mlflow.start_run():
        params = {"max_depth": 6, "n_estimators": 200, "learning_rate": 0.1}
        mlflow.log_params(params)

        model = xgb.XGBClassifier(**params, use_label_encoder=False, eval_metric="auc")
        model.fit(X_train, y_train)

        preds_proba = model.predict_proba(X_test)[:,1]
        auc = roc_auc_score(y_test, preds_proba)
        mlflow.log_metric("auc", float(auc))

        # optional: compute precision/recall at threshold 0.5
        preds = (preds_proba >= 0.5).astype(int)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, preds, average="binary", zero_division=0)
        mlflow.log_metric("precision", float(prec))
        mlflow.log_metric("recall", float(rec))
        mlflow.log_metric("f1", float(f1))

        # Save the model artifact
        model_path = "model.joblib"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path, artifact_path="model")

        print("Trained model AUC:", auc)
        print("Saved model to", model_path)

if __name__ == "__main__":
    main()
