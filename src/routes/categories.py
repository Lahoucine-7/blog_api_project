"""
Routes pour la gestion des catégories.

Fournit les endpoints CRUD pour l'entité Categorie.
"""

from flask import Blueprint, request, jsonify, abort
from src.models import db, Categorie

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


def get_or_404(model, pk):
    """Retourne l'instance du modèle ou renvoie 404 si non trouvée."""
    obj = db.session.get(model, pk)
    if obj is None:
        abort(404, description=f"{model.__name__} with id {pk} not found.")
    return obj


@categories_bp.route("", methods=["GET"])
def get_categories():
    """Retourne la liste complète des catégories."""
    categories = db.session.query(Categorie).all()
    return jsonify([categorie.to_dict() for categorie in categories]), 200


@categories_bp.route("/<int:categorie_id>", methods=["GET"])
def get_category(categorie_id: int):
    """Retourne une catégorie par son identifiant."""
    categorie = get_or_404(Categorie, categorie_id)
    return jsonify(categorie.to_dict()), 200


@categories_bp.route("", methods=["POST"])
def create_category():
    """Crée une nouvelle catégorie."""
    data = request.get_json()
    if not data or not data.get("nom"):
        return jsonify({"error": "Le nom de la catégorie est requis."}), 400
    new_category = Categorie(nom=data.get("nom"), description=data.get("description"))
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201


@categories_bp.route("/<int:categorie_id>", methods=["PUT"])
def update_category(categorie_id: int):
    """Met à jour une catégorie existante."""
    categorie = get_or_404(Categorie, categorie_id)
    data = request.get_json()
    if "nom" in data:
        categorie.nom = data["nom"]
    if "description" in data:
        categorie.description = data["description"]
    db.session.commit()
    return jsonify(categorie.to_dict()), 200


@categories_bp.route("/<int:categorie_id>", methods=["DELETE"])
def delete_category(categorie_id: int):
    """Supprime une catégorie par son identifiant."""
    categorie = get_or_404(Categorie, categorie_id)
    db.session.delete(categorie)
    db.session.commit()
    return jsonify({"message": "Catégorie supprimée."}), 200
