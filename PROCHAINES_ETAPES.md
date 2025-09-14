# Prochaines Étapes pour l'Assistant Web Éducatif

Ce document détaille les prochaines étapes de développement pour faire évoluer le projet de son état actuel (backend fonctionnel) vers une application complète, en se basant sur le cahier des charges et la vision du produit.

---
### Phase 1 : Consolidation du Backend et de l'API

L'objectif est de rendre le backend plus robuste et complet.

1.  **Gestion des Téléversements de Fichiers (Uploads) :**
    * [cite_start]Modifier l'endpoint `POST /documents` pour accepter un **vrai téléversement de fichier PDF** au lieu d'un simple nom de fichier [cite: 244-247, 305-309].
    * Sauvegarder le fichier téléversé dans le dossier `data/documents`.
    * Déclencher automatiquement le processus d'extraction et de vectorisation juste après le téléversement.

2.  **Affiner le Modèle de Réponse :**
    * [cite_start]Enrichir la réponse de l'API `/ask` pour inclure les **sources exactes** (nom du document, numéro de page, etc.) qui ont servi de contexte [cite: 269-277].
    * Cela implique de stocker plus de métadonnées (comme le numéro de page) lors du découpage du texte.

3.  **Gestion des Utilisateurs :**
    * [cite_start]Créer des modèles de données et des tables pour les **utilisateurs** (Étudiant, Enseignant, Administrateur) [cite: 1236-1240, 1253-1255].
    * [cite_start]Mettre en place un système d'**authentification** (par exemple, avec JWT) pour sécuriser les endpoints[cite: 71, 132].

---
### Phase 2 : Développement du Frontend

L'objectif est de créer une interface utilisateur pour interagir avec le backend.

1.  **Interface de Questions-Réponses :**
    * [cite_start]Créer une page simple avec un champ de saisie pour poser une question et une zone pour afficher la réponse de l'IA [cite: 258-260, 1142].
    * Connecter cette interface à l'endpoint `/api/v1/ask`.

2.  **Interface d'Administration :**
    * [cite_start]Développer une page sécurisée pour les enseignants et administrateurs[cite: 236].
    * [cite_start]Créer un formulaire pour le **téléversement des manuels PDF** [cite: 237-242].
    * Afficher la liste des documents déjà présents dans le système.

---
### Phase 3 : Améliorations et Déploiement

L'objectif est de préparer le projet pour une utilisation réelle.

1.  **Amélioration de la Pertinence :**
    * [cite_start]Explorer des **modèles de `sentence-transformers` multilingues** ou plus spécialisés en science pour améliorer la qualité de la recherche sémantique[cite: 80].
    * [cite_start]Permettre à l'utilisateur de noter la pertinence des réponses pour un apprentissage continu (auto-amélioration)[cite: 20, 1271].

2.  **Mise en place du Cache :**
    * [cite_start]Intégrer **Redis** pour mettre en cache les questions fréquentes et accélérer les temps de réponse, comme spécifié dans l'architecture[cite: 25, 62, 1384].

3.  **Conteneurisation Complète avec Docker Compose :**
    * [cite_start]Écrire un fichier `docker-compose.yml` pour lancer toute l'application (Backend, PostgreSQL, Redis, Ollama) avec une seule commande, simplifiant ainsi le déploiement [cite: 148-193].
