# Assistant Web Éducatif - API Backend

Ce dépôt contient le code source du backend pour l'Assistant Web Éducatif. C'est une API développée en Python avec FastAPI qui fournit la logique pour traiter des documents et répondre à des questions en utilisant un modèle de langage local.

## État Actuel

Le projet est une base fonctionnelle qui inclut :
-   Une API pour la gestion des métadonnées de documents (créer, lister).
-   Une chaîne de traitement complète pour les fichiers PDF : extraction de texte, découpage, et vectorisation.
-   Un endpoint de questions-réponses qui interroge une base de données vectorielle et génère des réponses avec un LLM via Ollama.

## Stack Technique

-   **Framework API :** FastAPI
-   **Base de données (Métadonnées) :** PostgreSQL (lancé avec Docker)
-   **Base de données (Vecteurs) :** ChromaDB
-   **Modèles de Langage (LLM) :** Ollama (avec le modèle Mistral)
-   **Traitement de texte & Vectorisation :** LangChain, Sentence-Transformers, PyMuPDF
-   **ORM :** SQLAlchemy

## Démarrage Rapide

1.  **Prérequis :** Assurez-vous d'avoir Python 3.9+, Docker et Ollama installés.

2.  **Clonez le dépôt :**
    ```bash
    git clone [https://github.com/Mawandu/Assistant-Web-Educatif.git](https://github.com/Mawandu/Assistant-Web-Educatif.git)
    cd Assistant-Web-Educatif
    ```

3.  **Installez les dépendances Python :**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **Lancez les services externes :**
    - **PostgreSQL :**
      ```bash
      docker run -d --name postgres-assistantWed -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=assistantWed_db -p 5432:5432 postgres:13
      ```
    - **Ollama :** (dans un autre terminal)
      ```bash
      ollama pull mistral
      ollama serve
      ```

5.  **Initialisez la base de données :**
    ```bash
    python -m scripts.init_db
    ```

6.  **Lancez le serveur API :**
    ```bash
    uvicorn backend.main:app --reload
    ```
L'API est maintenant accessible à `http://127.0.0.1:8000` et la documentation interactive à `http://127.0.0.1:8000/docs`.
