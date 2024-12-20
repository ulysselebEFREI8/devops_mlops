import os
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data():
    """Charger et prétraiter les données d'entraînement."""
    csv_path = os.path.join(os.path.dirname(__file__), 'kc_house_data.csv')
    df = pd.read_csv(csv_path)

    # Sélectionner les colonnes pertinentes
    df = df[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'waterfront', 'condition', 'grade', 'yr_built']]

    # Encodage des colonnes catégorielles
    label_encoder = LabelEncoder()
    df['waterfront'] = label_encoder.fit_transform(df['waterfront'])
    df['condition'] = label_encoder.fit_transform(df['condition'])
    df['grade'] = label_encoder.fit_transform(df['grade'])

    return df

def train_model():
    """Entraîner et enregistrer le modèle avec MLflow."""
    df = load_data()
    X = df.drop(columns='price')
    y = df['price']

    # Division des données
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Enregistrer le modèle dans MLflow
    with mlflow.start_run():
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="HousePriceModel"
        )
        r2_score = model.score(X_test, y_test)
        mlflow.log_metric("r2_score", r2_score)
        print(f"Modèle R^2 Score: {r2_score}")

if __name__ == "__main__":
    train_model()
