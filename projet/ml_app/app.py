import pandas as pd
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

csv_path = os.path.join(os.path.dirname(__file__), 'kc_house_data.csv')

# Liste pour stocker les prédictions
predictions_list = []

# Charger le dataset
df = pd.read_csv(csv_path)

# Prétraiter les données
# On sélectionne les colonnes pertinentes pour l'entraînement du modèle
df = df[['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'waterfront', 'condition', 'grade', 'yr_built']]

# Encodage des colonnes catégorielles (par exemple, 'waterfront', 'view', 'condition', etc.)
label_encoder = LabelEncoder()
df['waterfront'] = label_encoder.fit_transform(df['waterfront'])
df['condition'] = label_encoder.fit_transform(df['condition'])
df['grade'] = label_encoder.fit_transform(df['grade'])

# Définir les features et la cible
X = df.drop('price', axis=1)  # Features (tout sauf 'price')
y = df['price']  # Target (le prix)

# Diviser les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Sauvegarder le modèle une seule fois
joblib.dump(model, 'house_price_model.pkl')

# Charger le modèle une seule fois au démarrage de l'application
model = joblib.load('house_price_model.pkl')

# Route pour afficher la page de prédiction
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Récupérer les données envoyées par le formulaire
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        sqft_living = float(request.form['sqft_living'])* 10.7639
        sqft_lot = float(request.form['sqft_lot'])* 10.7639 #convert m2 to sqrt
        waterfront = int(request.form['waterfront'])
        condition = int(request.form['condition'])
        grade = int(request.form['grade'])
        yr_built = int(request.form['yr_built'])

        # Créer un tableau des caractéristiques d'entrée
        features = np.array([[bedrooms, bathrooms, sqft_living, sqft_lot, waterfront, condition, grade, yr_built]])

       # Charger le  modèle préalablement sauvegardé
        model = joblib.load('house_price_model.pkl')

        # Faire la prédiction
        prediction = model.predict(features)[0]

	# Ajouter la prédiction à la liste des prédictions
        predictions_list.append(prediction)

        return render_template('predict.html', prediction=prediction)

    return render_template('predict.html', prediction=None)


@app.route('/monitoring')
def monitoring():
    # Calculer des statistiques simples sur les prix prédits
    if predictions_list:  # Vérifier si la liste de prédictions n'est pas vide
        mean_prediction = np.mean(predictions_list)
        median_prediction = np.median(predictions_list)
        max_prediction = np.max(predictions_list)
    else:
        mean_prediction = median_prediction = max_prediction = 0

    stats = {
        'mean_price': df['price'].mean(),
        'median_price': df['price'].median(),
        'max_price': df['price'].max(),
        'mean_prediction': mean_prediction,
        'median_prediction': median_prediction,
        'max_prediction': max_prediction,
    }
    return render_template('monitoring.html', stats=stats)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

