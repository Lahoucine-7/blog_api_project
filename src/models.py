"""
Définition des modèles de données pour le projet.

Ce module définit les entités Utilisateur, Categorie, Article et Commentaire,
leurs relations et leur méthode de sérialisation.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Utilisateur(db.Model):
    """
    Modèle Utilisateur.

    Attributs:
        id : Identifiant unique.
        nom : Nom de l'utilisateur.
        email : Email unique de l'utilisateur.
    """

    __tablename__ = "utilisateurs"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)

    # Relations
    articles = db.relationship(
        "Article", back_populates="utilisateur", cascade="all, delete-orphan"
    )
    commentaires = db.relationship(
        "Commentaire", back_populates="utilisateur", cascade="all, delete-orphan"
    )

    def __init__(self, nom: str, email: str) -> None:
        """Initialise un utilisateur avec un nom et un email."""
        self.nom = nom
        self.email = email

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de l'utilisateur."""
        return {"id": self.id, "nom": self.nom, "email": self.email}


class Categorie(db.Model):
    """
    Modèle Categorie.

    Attributs:
        id : Identifiant unique.
        nom : Nom unique de la catégorie.
        description : Description facultative.
    """

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    # Relation: une catégorie contient plusieurs articles
    articles = db.relationship(
        "Article", back_populates="categorie", cascade="all, delete-orphan"
    )

    def __init__(self, nom: str, description: str = "") -> None:
        """Initialise une catégorie."""
        self.nom = nom
        self.description = description

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de la catégorie."""
        return {"id": self.id, "nom": self.nom, "description": self.description}


class Article(db.Model):
    """
    Modèle Article.

    Attributs:
        id : Identifiant unique.
        titre : Titre de l'article.
        contenu : Contenu de l'article.
        date_publication : Date de publication (définie par défaut).
        categorie_id : Clé étrangère vers Categorie.
        auteur_id : Clé étrangère vers Utilisateur.
    """

    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(255), nullable=False)
    contenu = db.Column(db.Text)
    date_publication = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.now()
    )
    categorie_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    auteur_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)

    # Relations
    categorie = db.relationship("Categorie", back_populates="articles")
    utilisateur = db.relationship("Utilisateur", back_populates="articles")
    commentaires = db.relationship(
        "Commentaire", back_populates="article", cascade="all, delete-orphan"
    )

    def __init__(
        self, titre: str, contenu: str, categorie_id: int, auteur_id: int
    ) -> None:
        """Initialise un article."""
        self.titre = titre
        self.contenu = contenu
        self.categorie_id = categorie_id
        self.auteur_id = auteur_id

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire de l'article."""
        return {
            "id": self.id,
            "titre": self.titre,
            "contenu": self.contenu,
            "date_publication": (
                self.date_publication.isoformat() if self.date_publication else None
            ),
            "categorie_id": self.categorie_id,
            "auteur_id": self.auteur_id,
        }


class Commentaire(db.Model):
    """
    Modèle Commentaire.

    Attributs:
        id : Identifiant unique.
        contenu : Contenu du commentaire.
        date_commentaire : Date de création (par défaut).
        article_id : Clé étrangère vers Article.
        auteur_id : Clé étrangère vers Utilisateur.
    """

    __tablename__ = "commentaires"
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_commentaire = db.Column(
        db.TIMESTAMP(timezone=True), server_default=db.func.now()
    )
    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"), nullable=False)
    auteur_id = db.Column(db.Integer, db.ForeignKey("utilisateurs.id"), nullable=False)

    # Relations
    article = db.relationship("Article", back_populates="commentaires")
    utilisateur = db.relationship("Utilisateur", back_populates="commentaires")

    def __init__(self, contenu: str, article_id: int, auteur_id: int) -> None:
        """Initialise un commentaire."""
        self.contenu = contenu
        self.article_id = article_id
        self.auteur_id = auteur_id

    def to_dict(self) -> dict:
        """Retourne une représentation dictionnaire du commentaire."""
        return {
            "id": self.id,
            "contenu": self.contenu,
            "date_commentaire": (
                self.date_commentaire.isoformat() if self.date_commentaire else None
            ),
            "article_id": self.article_id,
            "auteur_id": self.auteur_id,
        }
