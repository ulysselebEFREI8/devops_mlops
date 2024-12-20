#!/bin/bash

# Créer le répertoire des logs s'il n'existe pas déjà
mkdir -p /app/logs

# Lancer supervisord pour gérer les processus en arrière-plan
exec supervisord -c /etc/supervisor/conf.d/supervisord.conf

# Maintenir le conteneur en cours d'exécution
tail -f /dev/null
