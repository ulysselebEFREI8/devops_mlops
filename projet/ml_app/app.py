import os
import numpy as np
from flask import Flask, render_template, request, jsonify
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.tracking import MlflowClient

app = Flask(__name__)

# Définir l'URI de suivi de MLflow pour pointer vers le répertoire des artefacts
os.environ["MLFLOW_TRACKING_URI"] = "file:///app/mlruns"

# Charger dynamiquement la dernière version du modèle depuis MLflow
MODEL_NAME = "HousePriceModel"

def load_latest_model():
    """Charger automatiquement la dernière version du modèle depuis MLflow."""
    try:
        # Créer un client MLflow
        client = MlflowClient()

        # Récupérer la dernière version du modèle avec le stage 'Production' ou 'None'
        latest_version_info = client.get_latest_versions(MODEL_NAME, stages=["Production", "None"])

        if latest_version_info:
            # Récupérer l'ID du run
            latest_run_id = latest_version_info[0].run_id
            print(f"L'ID du run pour la dernière version du modèle est : {latest_run_id}")

            # Charger le modèle avec l'ID du run
            model_uri = f"file:/app/mlruns/0/{latest_run_id}/artifacts/model"
            model = mlflow.sklearn.load_model(model_uri)
            print(f"Modèle {MODEL_NAME} chargé avec succès.")
        else:
            raise Exception(f"Aucune version du modèle '{MODEL_NAME}' trouvée.")

    except Exception as e:
        raise Exception(f"Erreur lors du chargement du modèle : {str(e)}")

    return model

model = load_latest_model()

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
            features = pd.DataFrame([{
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'sqft_living': sqft_living,
                'sqft_lot': sqft_lot,
                'waterfront': waterfront,
                'condition': condition,
                'grade': grade,
                'yr_built': yr_built
            }])
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
def mlflow_page():
    """Redirection vers l'interface MLflow."""
    return render_template('mlflow.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/mlflow_proxy')
def mlflow_proxy():
    """Proxy to MLflow UI."""
    return jsonify({"message": "Redirecting to MLflow"}), 302, {"Location": "http://localhost:8001"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
