"""
Routes pour la gestion des articles.

Fournit les endpoints CRUD pour l'entité Article.
Utilise db.session.get() et un helper get_or_404() pour la compatibilité SQLAlchemy 2.0.
"""

from flask import Blueprint, request, jsonify, abort
from src.models import db, Article, Categorie, Utilisateur

articles_bp = Blueprint("articles", __name__, url_prefix="/articles")


def get_or_404(model, pk):
    """
    Retourne l'instance du modèle correspondant à la clé primaire pk,
    ou renvoie une erreur 404 si non trouvée.
    """
    obj = db.session.get(model, pk)
    if obj is None:
        abort(404, description=f"{model.__name__} with id {pk} not found.")
    return obj


@articles_bp.route("", methods=["GET"])
def get_articles():
    """Retourne la liste complète des articles."""
    articles = db.session.query(Article).all()
    return jsonify([article.to_dict() for article in articles]), 200


@articles_bp.route("/<int:article_id>", methods=["GET"])
def get_article(article_id: int):
    """Retourne un article par son identifiant."""
    article = get_or_404(Article, article_id)
    return jsonify(article.to_dict()), 200


@articles_bp.route("", methods=["POST"])
def create_article():
    """Crée un nouvel article en fonction des données JSON fournies."""
    data = request.get_json()
    if not data or not data.get("titre") or not data.get("contenu"):
        return jsonify({"error": "Titre et contenu sont requis."}), 400

    categorie = db.session.get(Categorie, data.get("categorie_id"))
    utilisateur = db.session.get(Utilisateur, data.get("auteur_id"))
    if not categorie or not utilisateur:
        return jsonify({"error": "Catégorie ou utilisateur invalide."}), 400

    new_article = Article(
        titre=data.get("titre"),
        contenu=data.get("contenu"),
        categorie_id=data.get("categorie_id"),
        auteur_id=data.get("auteur_id"),
    )
    db.session.add(new_article)
    db.session.commit()
    return jsonify(new_article.to_dict()), 201


@articles_bp.route("/<int:article_id>", methods=["PUT"])
def update_article(article_id: int):
    """Met à jour un article existant."""
    article = get_or_404(Article, article_id)
    data = request.get_json()
    if "titre" in data:
        article.titre = data["titre"]
    if "contenu" in data:
        article.contenu = data["contenu"]
    if "categorie_id" in data:
        categorie = db.session.get(Categorie, data["categorie_id"])
        if not categorie:
            return jsonify({"error": "Catégorie invalide."}), 400
        article.categorie_id = data["categorie_id"]
    if "auteur_id" in data:
        utilisateur = db.session.get(Utilisateur, data["auteur_id"])
        if not utilisateur:
            return jsonify({"error": "Utilisateur invalide."}), 400
        article.auteur_id = data["auteur_id"]
    db.session.commit()
    return jsonify(article.to_dict()), 200


@articles_bp.route("/<int:article_id>", methods=["DELETE"])
def delete_article(article_id: int):
    """Supprime un article par son identifiant."""
    article = get_or_404(Article, article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({"message": "Article supprimé."}), 200
