```markdown
# 🚀 Blog API avec Intégration d'une Base de Données SQL

## 📝 Description du Projet

Ce projet a pour objectif de concevoir et d’implémenter l’intégration d’une base de données SQL dans le cadre d’un blog.  
Il fournit une API RESTful permettant la gestion complète des contenus du blog – articles, catégories, commentaires et utilisateurs – via des opérations CRUD.

**Note :** Ce projet est un projet personnel réalisé dans un but d'apprentissage. Il n'est **pas destiné à un usage en production**.

---

## 🎯 Contexte et Objectifs

Le client est un éditeur de contenu en ligne souhaitant moderniser son infrastructure technique.  
L'API doit permettre :

- La conception d’un schéma relationnel pour un blog.
- L’implémentation de CRUD complet via une API REST.
- L’optimisation des requêtes SQL.
- Une bonne couverture de tests pour garantir la robustesse.

---

## 🛠️ Stack Technologique

- **Langage & Environnement :** Python (≥ 3.9)
- **Framework :** Flask
- **Base de Données :** PostgreSQL
- **ORM :** SQLAlchemy (compatible 2.0)
- **Migrations :** Flask-Migrate (Alembic)
- **Tests :** Unittest (+ possibilité d'utiliser Pytest)
- **Configuration :** python-dotenv
- **Versionnement :** Git

---

## ⚙️ Installation et Configuration

### 📦 Prérequis

- Python 3.9 ou supérieur
- PostgreSQL installé et configuré
- Git

### 🛠️ Étapes d'Installation

1. **Cloner le dépôt :**

    ```bash
    git clone <URL_DU_DEPOT>
    cd blog_api_project
    ```

2. **Créer et activer l’environnement virtuel :**

    ```bash
    python -m venv venv
    ```

    Linux/Mac :

    ```bash
    source venv/bin/activate
    ```

    Windows :

    ```bash
    venv\Scripts\activate
    ```

3. **Installer les dépendances :**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurer les Variables d'Environnement :**

    Créer un fichier `.env` :

    ```bash
    DATABASE_URL=postgresql://blog_user:admin@localhost/blog_db
    TESTING=False
    ```

5. **Initialiser la Base de Données :**

    Option 1 – Script rapide :

    ```bash
    python -m src.create_db
    ```

    Option 2 – Avec Flask-Migrate :

    ```bash
    flask db init
    flask db migrate -m "Initial migration: création des tables"
    flask db upgrade
    ```

---

## 📡 Utilisation de l'API

### 🚀 Démarrer le Serveur

    ```bash
    python -m src.app
    ```

Le serveur sera disponible sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### 🛤️ Endpoints Disponibles

#### 🔹 Utilisateurs

- `GET /utilisateurs` → Liste des utilisateurs
- `GET /utilisateurs/<id>` → Détail d'un utilisateur
- `POST /utilisateurs` → Créer un utilisateur
- `PUT /utilisateurs/<id>` → Mettre à jour un utilisateur
- `DELETE /utilisateurs/<id>` → Supprimer un utilisateur

#### 🔹 Catégories

- `GET /categories`
- `GET /categories/<id>`
- `POST /categories`
- `PUT /categories/<id>`
- `DELETE /categories/<id>`

#### 🔹 Articles

- `GET /articles`
- `GET /articles/<id>`
- `POST /articles`
- `PUT /articles/<id>`
- `DELETE /articles/<id>`

#### 🔹 Commentaires

- `GET /commentaires`
- `GET /commentaires/<id>`
- `POST /commentaires`
- `PUT /commentaires/<id>`
- `DELETE /commentaires/<id>`

---

## ✅ Exécution des Tests

Depuis la racine du projet :

    ```bash
    python -m unittest discover tests
    ```

Ou avec Pytest :

    ```bash
    pytest
    ```

Les tests couvrent :

- Création / Lecture / Mise à jour / Suppression pour **Utilisateurs**, **Catégories**, **Articles**, **Commentaires**.
- Cas normaux et cas d'erreurs.

---

## 🗂️ Schéma de la Base de Données

Le dossier `/docs` contient :

- `Diagramme.png` → Diagramme relationnel visuel
- `script_sql.sql` → Script SQL de création de la base

---

## 🧹 Optimisations et Bonnes Pratiques

- ✅ Utilisation de SQLAlchemy 2.0 (`db.session.get()` pour éviter les warnings)
- ✅ Gestion globale des erreurs Flask pour API plus propre
- ✅ Variables sensibles sécurisées via `.env`
- ✅ Modularité avancée (blueprints, modèles clairs)
- ✅ Excellente couverture de tests unitaires

---

## ⚠️ Remarques Importantes

- Ce projet est **fictif** et destiné uniquement à un **usage pédagogique**.
- Avant un déploiement réel, il serait nécessaire de renforcer la sécurité (authentification, validation avancée, contrôle d’accès).

---

## 📄 Licence

Projet sous licence **MIT**.
```
