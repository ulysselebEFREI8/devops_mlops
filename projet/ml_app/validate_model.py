import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def load_data():
    """ Charger et prétraiter les données d'entraînement. """
    csv_path = 'kc_house_data.csv'
    df = pd.read_csv(csv_path)

    # Sélectionner les colonnes pertinentes
    df = df[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'waterfront', 'condition', 'grade', 'yr_built']]

    # Encodage des colonnes catégorielles
    label_encoder = LabelEncoder()
    df['waterfront'] = label_encoder.fit_transform(df['waterfront'])
    df['condition'] = label_encoder.fit_transform(df['condition'])
    df['grade'] = label_encoder.fit_transform(df['grade'])

    return df

def validate_model():
    """ Charger et tester le modèle enregistré avec MLflow. """
    # Charger les données de validation
    df = load_data()
    X = df.drop(columns='price')
    y = df['price']
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Charger le modèle depuis MLflow
    model_uri = "models:/HousePriceModel/latest"
    model = mlflow.pyfunc.load_model(model_uri)

    # Prédire avec le modèle
    y_pred = model.predict(X_test)

    # Calculer l'erreur quadratique moyenne (MSE)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error (MSE): {mse}")

if __name__ == "__main__":
    validate_model()
