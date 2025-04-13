"""
Application Flask principale.

Ce fichier configure l'application, initialise l'instance SQLAlchemy et Flask-Migrate,
importe les blueprints des routes et définit un gestionnaire global d'erreurs.
La configuration se fait via des variables d'environnement pour plus de sécurité.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
from src.models import db

# Charger les variables d'environnement depuis un fichier .env si présent
load_dotenv()


def create_app() -> Flask:
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    # Configuration via des variables d'environnement
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://blog_user:admin@localhost/blog_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = os.getenv("TESTING", False)

    # Initialiser SQLAlchemy à partir du package models
    db.init_app(app)

    # Initialiser Flask-Migrate
    Migrate(app, db)

    # Importer et enregistrer les blueprints des routes
    from src.routes.articles import articles_bp
    from src.routes.categories import categories_bp
    from src.routes.utilisateurs import utilisateurs_bp
    from src.routes.commentaires import commentaires_bp

    app.register_blueprint(articles_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(utilisateurs_bp)
    app.register_blueprint(commentaires_bp)

    # Gestion globale des erreurs
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Personnaliser cette fonction pour logger et formater les erreurs.
        response = {"error": str(e)}
        status_code = 500
        if hasattr(e, "code") and isinstance(e.code, int):
            status_code = e.code
        return jsonify(response), status_code

    return app


# Création de l'application à utiliser dans tous les modules
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
