#!/bin/sh

echo "En attente de PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL démarré."

# Créer les tables de la base de données
echo "Initialisation de la base de données..."
python -m scripts.init_db

# Lancer le serveur Uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000
