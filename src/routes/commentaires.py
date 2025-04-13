"""
Routes pour la gestion des commentaires.

Fournit les endpoints CRUD pour l'entité Commentaire.
"""

from flask import Blueprint, request, jsonify, abort
from src.models import db, Commentaire, Article, Utilisateur

commentaires_bp = Blueprint("commentaires", __name__, url_prefix="/commentaires")


def get_or_404(model, pk):
    """Retourne l'instance du modèle ou renvoie 404 si non trouvée."""
    obj = db.session.get(model, pk)
    if obj is None:
        abort(404, description=f"{model.__name__} with id {pk} not found.")
    return obj


@commentaires_bp.route("", methods=["GET"])
def get_commentaires():
    """Retourne la liste complète des commentaires."""
    commentaires = db.session.query(Commentaire).all()
    return jsonify([commentaire.to_dict() for commentaire in commentaires]), 200


@commentaires_bp.route("/<int:commentaire_id>", methods=["GET"])
def get_commentaire(commentaire_id: int):
    """Retourne un commentaire par son identifiant."""
    commentaire = get_or_404(Commentaire, commentaire_id)
    return jsonify(commentaire.to_dict()), 200


@commentaires_bp.route("", methods=["POST"])
def create_commentaire():
    """Crée un nouveau commentaire."""
    data = request.get_json()
    if not data or not data.get("contenu"):
        return jsonify({"error": "Le contenu du commentaire est requis."}), 400

    article = db.session.get(Article, data.get("article_id"))
    utilisateur = db.session.get(Utilisateur, data.get("auteur_id"))
    if not article or not utilisateur:
        return jsonify({"error": "Article ou utilisateur invalide."}), 400

    new_commentaire = Commentaire(
        contenu=data.get("contenu"),
        article_id=data.get("article_id"),
        auteur_id=data.get("auteur_id"),
    )
    db.session.add(new_commentaire)
    db.session.commit()
    return jsonify(new_commentaire.to_dict()), 201


@commentaires_bp.route("/<int:commentaire_id>", methods=["PUT"])
def update_commentaire(commentaire_id: int):
    """Met à jour un commentaire existant."""
    commentaire = get_or_404(Commentaire, commentaire_id)
    data = request.get_json()
    if "contenu" in data:
        commentaire.contenu = data["contenu"]
    db.session.commit()
    return jsonify(commentaire.to_dict()), 200


@commentaires_bp.route("/<int:commentaire_id>", methods=["DELETE"])
def delete_commentaire(commentaire_id: int):
    """Supprime un commentaire par son identifiant."""
    commentaire = get_or_404(Commentaire, commentaire_id)
    db.session.delete(commentaire)
    db.session.commit()
    return jsonify({"message": "Commentaire supprimé."}), 200
