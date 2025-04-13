"""
Routes pour la gestion des utilisateurs.

Fournit les endpoints CRUD pour l'entité Utilisateur.
"""

from flask import Blueprint, request, jsonify, abort
from src.models import db, Utilisateur

utilisateurs_bp = Blueprint("utilisateurs", __name__, url_prefix="/utilisateurs")


def get_or_404(model, pk):
    """Retourne l'instance du modèle ou renvoie 404 si non trouvée."""
    obj = db.session.get(model, pk)
    if obj is None:
        abort(404, description=f"{model.__name__} with id {pk} not found.")
    return obj


@utilisateurs_bp.route("", methods=["GET"])
def get_utilisateurs():
    """Retourne la liste complète des utilisateurs."""
    utilisateurs = db.session.query(Utilisateur).all()
    return jsonify([utilisateur.to_dict() for utilisateur in utilisateurs]), 200


@utilisateurs_bp.route("/<int:utilisateur_id>", methods=["GET"])
def get_utilisateur(utilisateur_id: int):
    """Retourne un utilisateur par son identifiant."""
    utilisateur = get_or_404(Utilisateur, utilisateur_id)
    return jsonify(utilisateur.to_dict()), 200


@utilisateurs_bp.route("", methods=["POST"])
def create_utilisateur():
    """Crée un nouvel utilisateur."""
    data = request.get_json()
    if not data or not data.get("nom") or not data.get("email"):
        return jsonify({"error": "Le nom et l'email sont requis."}), 400
    new_utilisateur = Utilisateur(nom=data.get("nom"), email=data.get("email"))
    db.session.add(new_utilisateur)
    db.session.commit()
    return jsonify(new_utilisateur.to_dict()), 201


@utilisateurs_bp.route("/<int:utilisateur_id>", methods=["PUT"])
def update_utilisateur(utilisateur_id: int):
    """Met à jour un utilisateur existant."""
    utilisateur = get_or_404(Utilisateur, utilisateur_id)
    data = request.get_json()
    if "nom" in data:
        utilisateur.nom = data["nom"]
    if "email" in data:
        utilisateur.email = data["email"]
    db.session.commit()
    return jsonify(utilisateur.to_dict()), 200


@utilisateurs_bp.route("/<int:utilisateur_id>", methods=["DELETE"])
def delete_utilisateur(utilisateur_id: int):
    """Supprime un utilisateur par son identifiant."""
    utilisateur = get_or_404(Utilisateur, utilisateur_id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé."}), 200
