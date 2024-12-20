# Utilisation d'une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Créer le répertoire pour les logs de Flask et MLflow
RUN mkdir -p /app/logs
RUN chmod -R 777 /app/logs  # Assure que tout le monde peut lire/écrire dans /app/logs

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer Supervisor pour gérer les processus
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copier tous les fichiers de l'application dans le répertoire de travail
COPY . /app/

# Copier le fichier supervisord.conf dans le conteneur
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copier le script entrypoint.sh dans le conteneur
COPY entrypoint.sh /entrypoint.sh

# Rendre le script exécutable
RUN chmod +x /entrypoint.sh

# Exposer les ports nécessaires
EXPOSE 8000 8001

# Utiliser le script comme point d'entrée
ENTRYPOINT ["/entrypoint.sh"]
