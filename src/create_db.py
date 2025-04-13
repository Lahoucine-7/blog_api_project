"""
Script de création de la base de données.

Ce script est utile pour initialiser la base de données hors du contexte de migration.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from src.models import db


# La chaîne de connexion peut être récupérée via une variable d'environnement
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://blog_user:admin@localhost/blog_db"
)
engine = create_engine(DATABASE_URL)
db.metadata.create_all(engine)
