import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def load_data():
    """ Charger et prétraiter les données d'entraînement. """
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
    """ Entraîner et sauvegarder le modèle. """
    df = load_data()
    X = df.drop(columns='price')
    y = df['price']

    # Division des données
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Sauvegarder le modèle
    model_path = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
    joblib.dump(model, model_path)
    print(f"Modèle sauvegardé sous : {model_path}")

if __name__ == "__main__":
    train_model()
