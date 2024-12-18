import os
import numpy as np
from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Charger le modèle au démarrage
model_path = os.path.join(os.path.dirname(__file__), 'house_price_model.pkl')
model = joblib.load(model_path)

# Liste pour stocker les prédictions
predictions_list = []

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Récupérer les données
            bedrooms = int(request.form['bedrooms'])
            bathrooms = int(request.form['bathrooms'])
            sqft_living = float(request.form['sqft_living']) * 10.7639  # m2 -> sqft
            sqft_lot = float(request.form['sqft_lot']) * 10.7639  # m2 -> sqft
            waterfront = int(request.form['waterfront'])
            condition = int(request.form['condition'])
            grade = int(request.form['grade'])
            yr_built = int(request.form['yr_built'])

            # Créer un tableau des caractéristiques d'entrée
            features = np.array([[bedrooms, bathrooms, sqft_living, sqft_lot, waterfront, condition, grade, yr_built]])
            prediction = model.predict(features)[0]
            predictions_list.append(prediction)

            return render_template('predict.html', prediction=prediction)
        except Exception as e:
            return f"Erreur lors de la prédiction : {str(e)}", 400

    return render_template('predict.html', prediction=None)

@app.route('/monitoring')
def monitoring():
    """Statistiques sur les prédictions."""
    if predictions_list:
        mean_prediction = np.mean(predictions_list)
        median_prediction = np.median(predictions_list)
        max_prediction = np.max(predictions_list)
    else:
        mean_prediction = median_prediction = max_prediction = 0

    stats = {
        'mean_prediction': mean_prediction,
        'median_prediction': median_prediction,
        'max_prediction': max_prediction
    }
    return render_template('monitoring.html', stats=stats)

@app.route('/mlflow')
def mlflow():
    """Redirection vers l'interface MLflow."""
    return render_template('mlflow.html')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
