# Assistant Web Éducatif - Full Stack

Ce dépôt contient le code source complet de l'Assistant Web Éducatif, une application full stack conçue pour aider les étudiants dans un domaine spécifique. Le système analyse des manuels PDF, permet de poser des questions en langage naturel et fournit des réponses sourcées grâce à un modèle de langage local.

## Fonctionnalités Principales ✨
-   **API Backend Robuste** : Construite avec FastAPI, elle gère la logique de traitement des documents, l'authentification des utilisateurs et la génération des réponses.
-   **Interface Frontend Interactive** : Développée avec React (Vite), elle offre une interface de chat pour les étudiants et un panneau d'administration pour les enseignants.
-   **Gestion des Utilisateurs** : Système d'authentification complet avec des rôles (étudiant, enseignant) pour sécuriser l'application.
-   **IA Locale et Privée** : Utilise Ollama pour faire tourner des modèles de langage localement, garantissant la confidentialité des données.
-   **Déploiement Simplifié** : L'ensemble de l'application (backend, frontend, base de données, IA) peut être lancé avec une seule commande grâce à Docker Compose.

## Stack Technique 🛠️
-   **Backend** : Python, FastAPI, SQLAlchemy
-   **Frontend** : JavaScript, React, Vite
-   **Base de données (Métadonnées)** : PostgreSQL
-   **Base de données (Vecteurs)** : ChromaDB
-   **Modèles de Langage (LLM)** : Ollama
-   **Conteneurisation** : Docker & Docker Compose

## Démarrage Rapide (Méthode Recommandée) 🚀

Cette méthode lance tous les services nécessaires avec une seule commande.

1.  **Prérequis** : Assurez-vous d'avoir **Docker** et **Docker Compose** installés. Si vous avez une carte graphique NVIDIA, installez également les drivers appropriés et le NVIDIA Container Toolkit.

2.  **Clonez le dépôt** :
    ```bash
    git clone [https://github.com/Mawandu/Assistant-Web-Educatif.git](https://github.com/Mawandu/Assistant-Web-Educatif.git)
    cd Assistant-Web-Educatif
    ```

3.  **Lancez l'application** :
    Cette commande va construire les images et démarrer tous les conteneurs.
    ```bash
    docker-compose up --build -d
    ```

4.  **Configurez les modèles d'IA** (la première fois seulement) :
    * Pendant que l'application tourne, ouvrez un nouveau terminal pour télécharger un modèle d'IA.
    * Lancez l'une des commandes suivantes :
        ```bash
        # Recommandé si vous avez peu de RAM (< 8Go)
        docker-compose exec ollama ollama pull tinyllama

        # Recommandé si vous avez plus de RAM (> 8Go)
        docker-compose exec ollama ollama pull mistral
        ```
    * **Important** : Assurez-vous que le nom du modèle que vous téléchargez correspond à celui utilisé dans votre code (`backend/services/ollama_client.py`).

5.  **Initialisation du premier utilisateur** (la première fois seulement) :
    * L'application est lancée mais la base de données est vide. Suivez ces étapes pour créer un compte enseignant.
    * **a. Créez les tables dans la base de données :**
        ```bash
        docker-compose exec backend python -m scripts.init_db
        ```
    * **b. Créez le compte utilisateur via l'API :**
        * Allez sur `http://localhost:8000/docs`.
        * Utilisez l'endpoint `POST /api/v1/users` pour créer un utilisateur (ex: `prof@test.com` avec un mot de passe).
    * **c. Donnez-lui le rôle "enseignant" :**
        ```bash
        docker-compose exec backend python -m scripts.set_user_role prof@test.com enseignant
        ```

Votre application est maintenant entièrement configurée et accessible :
-   **Frontend (Interface Utilisateur)** : `http://localhost:5173/`
-   **Backend (API Docs)** : `http://localhost:8000/docs`