"""
Tests unitaires pour les endpoints de commentaires.

Ce fichier teste la création, la récupération, la mise à jour et la suppression d'un commentaire.
"""

import json
import unittest
from src.app import app, db
from src.models import Utilisateur, Categorie, Article, Commentaire


class CommentairesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Créer un utilisateur et une catégorie pour créer un article.
            utilisateur = Utilisateur("Test User", "commentuser@example.com")
            categorie = Categorie("Catégorie Test", "Description de test")
            db.session.add(utilisateur)
            db.session.add(categorie)
            db.session.commit()
            # Créer un article
            article = Article(
                "Article Test", "Contenu pour commentaire", categorie.id, utilisateur.id
            )
            db.session.add(article)
            db.session.commit()
            self.article_id = article.id
            self.utilisateur_id = utilisateur.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_commentaire_valid(self):
        payload = {
            "contenu": "Commentaire de test",
            "article_id": self.article_id,
            "auteur_id": self.utilisateur_id,
        }
        response = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["contenu"], "Commentaire de test")
        self.assertEqual(data["article_id"], self.article_id)
        self.assertEqual(data["auteur_id"], self.utilisateur_id)

    def test_create_commentaire_missing_contenu(self):
        payload = {"article_id": self.article_id, "auteur_id": self.utilisateur_id}
        response = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_create_commentaire_invalid_article(self):
        payload = {
            "contenu": "Commentaire de test",
            "article_id": 9999,
            "auteur_id": self.utilisateur_id,
        }
        response = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_commentaires_and_commentaire_by_id(self):
        payload = {
            "contenu": "Commentaire pour get",
            "article_id": self.article_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        commentaire = json.loads(post_resp.data)
        cid = commentaire["id"]

        get_resp = self.client.get("/commentaires")
        self.assertEqual(get_resp.status_code, 200)
        commentaires = json.loads(get_resp.data)
        self.assertGreaterEqual(len(commentaires), 1)

        get_one_resp = self.client.get(f"/commentaires/{cid}")
        self.assertEqual(get_one_resp.status_code, 200)
        commentaire_fetched = json.loads(get_one_resp.data)
        self.assertEqual(commentaire_fetched["id"], cid)

    def test_update_commentaire(self):
        payload = {
            "contenu": "Commentaire Initial",
            "article_id": self.article_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        cid = json.loads(post_resp.data)["id"]

        update_payload = {"contenu": "Commentaire Modifié"}
        update_resp = self.client.put(
            f"/commentaires/{cid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)
        updated_commentaire = json.loads(update_resp.data)
        self.assertEqual(updated_commentaire["contenu"], "Commentaire Modifié")

    def test_delete_commentaire(self):
        payload = {
            "contenu": "Commentaire à supprimer",
            "article_id": self.article_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/commentaires", data=json.dumps(payload), content_type="application/json"
        )
        cid = json.loads(post_resp.data)["id"]

        delete_resp = self.client.delete(f"/commentaires/{cid}")
        self.assertEqual(delete_resp.status_code, 200)
        get_resp = self.client.get(f"/commentaires/{cid}")
        self.assertEqual(get_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
