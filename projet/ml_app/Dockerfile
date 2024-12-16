# Utiliser l'image officielle de Python 3.9 comme base
FROM python:3.9-slim

# Installer les dépendances nécessaires
RUN pip install flask numpy scikit-learn joblib

# Créer le répertoire de travail de l'application
WORKDIR /app

# Copier le fichier app.py dans le conteneur
COPY app.py /app

# Exposer le port 5000 pour accéder à l'application Flask
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["python", "app.py"]
