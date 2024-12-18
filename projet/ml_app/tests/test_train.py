import mlflow
import mlflow.sklearn
import os
import pytest
from sklearn.linear_model import LinearRegression
import joblib
import pandas as pd

# Charger les données (fonction existante dans ton code)
def load_data():
    df = pd.read_csv('kc_house_data.csv')
    df = df[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'waterfront', 'condition', 'grade', 'yr_built']]
    return df

# Tester si le modèle est bien enregistré dans MLflow
def test_mlflow_model_logging():
    df = load_data()
    X = df.drop(columns='price')
    y = df['price']
    model = LinearRegression()
    model.fit(X, y)

    with mlflow.start_run():
        mlflow.sklearn.log_model(model, "model", registered_model_name="HousePriceModel")

    # Vérifier que le modèle a été correctement enregistré
    model_uri = f"models:/HousePriceModel/1"
    model_from_mlflow = mlflow.sklearn.load_model(model_uri)
    assert model_from_mlflow is not None

# Tester si le R^2 est enregistré
def test_r2_score_logging():
    df = load_data()
    X = df.drop(columns='price')
    y = df['price']
    model = LinearRegression()
    model.fit(X, y)

    with mlflow.start_run():
        r2_score = model.score(X, y)
        mlflow.log_metric("r2_score", r2_score)

    # Vérifier que le R^2 a été enregistré
    run_id = mlflow.active_run().info.run_id
    logged_r2_score = mlflow.get_metric_history("r2_score", run_id)[-1].value
    assert logged_r2_score == pytest.approx(r2_score, rel=1e-2)
