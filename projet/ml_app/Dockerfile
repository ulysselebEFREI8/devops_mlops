# Utiliser l'image officielle de Python 3.9 comme base
FROM python:3.9-slim

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    supervisor && \
    pip install flask numpy scikit-learn joblib mlflow && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer les dossiers nécessaires
RUN mkdir -p /app /var/log/supervisor

# Copier les fichiers nécessaires
WORKDIR /app
COPY app.py /app/
COPY house_price_model.pkl /app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exposer les ports pour Flask et MLflow
EXPOSE 8000 8001

# Lancer supervisord pour gérer plusieurs processus
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
