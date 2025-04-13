# tests/test_articles.py
import json
import unittest
from src.app import app, db
from src.models import Utilisateur, Categorie, Article


class ArticlesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        # Base en mémoire pour les tests
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Crée un utilisateur et une catégorie pour tester la création d'article.
            utilisateur = Utilisateur("Test User", "articleuser@example.com")
            categorie = Categorie("Catégorie Test", "Description de test")
            db.session.add(utilisateur)
            db.session.add(categorie)
            db.session.commit()
            self.utilisateur_id = utilisateur.id
            self.categorie_id = categorie.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_article_valid(self):
        payload = {
            "titre": "Article Test",
            "contenu": "Contenu de l'article de test",
            "categorie_id": self.categorie_id,
            "auteur_id": self.utilisateur_id,
        }
        response = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["titre"], "Article Test")
        self.assertEqual(data["contenu"], "Contenu de l'article de test")
        self.assertEqual(data["categorie_id"], self.categorie_id)
        self.assertEqual(data["auteur_id"], self.utilisateur_id)

    def test_create_article_missing_fields(self):
        # Manque le titre et le contenu
        payload = {"categorie_id": self.categorie_id, "auteur_id": self.utilisateur_id}
        response = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_create_article_invalid_ids(self):
        # Utilise des IDs inexistants
        payload = {
            "titre": "Article Test",
            "contenu": "Contenu de test",
            "categorie_id": 9999,
            "auteur_id": 9999,
        }
        response = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_articles_and_article_by_id(self):
        # Créer un article
        payload = {
            "titre": "Article Pour Get",
            "contenu": "Contenu GET",
            "categorie_id": self.categorie_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        article = json.loads(post_resp.data)
        aid = article["id"]

        # Récupérer tous les articles
        get_resp = self.client.get("/articles")
        self.assertEqual(get_resp.status_code, 200)
        articles = json.loads(get_resp.data)
        self.assertGreaterEqual(len(articles), 1)

        # Récupérer l'article par son ID
        get_one_resp = self.client.get(f"/articles/{aid}")
        self.assertEqual(get_one_resp.status_code, 200)
        article_fetched = json.loads(get_one_resp.data)
        self.assertEqual(article_fetched["id"], aid)

    def test_update_article(self):
        # Créer un article
        payload = {
            "titre": "Article Initial",
            "contenu": "Contenu Initial",
            "categorie_id": self.categorie_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        article = json.loads(post_resp.data)
        aid = article["id"]

        # Mise à jour de l'article
        update_payload = {"titre": "Article Modifié", "contenu": "Contenu Modifié"}
        update_resp = self.client.put(
            f"/articles/{aid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)
        updated_article = json.loads(update_resp.data)
        self.assertEqual(updated_article["titre"], "Article Modifié")
        self.assertEqual(updated_article["contenu"], "Contenu Modifié")

    def test_delete_article(self):
        # Créer un article
        payload = {
            "titre": "Article À Supprimer",
            "contenu": "Contenu à supprimer",
            "categorie_id": self.categorie_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        aid = json.loads(post_resp.data)["id"]

        # Supprimer l'article
        delete_resp = self.client.delete(f"/articles/{aid}")
        self.assertEqual(delete_resp.status_code, 200)
        # Vérifier que l'article n'existe plus
        get_resp = self.client.get(f"/articles/{aid}")
        self.assertEqual(get_resp.status_code, 404)


class ArticlesExtraTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            utilisateur = Utilisateur("Extra User", "extra@example.com")
            categorie = Categorie("Extra Catégorie", "Extra description")
            db.session.add(utilisateur)
            db.session.add(categorie)
            db.session.commit()
            self.utilisateur_id = utilisateur.id
            self.categorie_id = categorie.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_article_invalid_json(self):
        # Test avec un mauvais format de données (non JSON)
        response = self.client.post(
            "/articles", data="not a json", content_type="application/json"
        )
        # Flask renverra 400 si get_json() échoue
        self.assertEqual(response.status_code, 400)

    def test_partial_update_article(self):
        # Créer un article
        payload = {
            "titre": "Partial Update Test",
            "contenu": "Initial Content",
            "categorie_id": self.categorie_id,
            "auteur_id": self.utilisateur_id,
        }
        post_resp = self.client.post(
            "/articles", data=json.dumps(payload), content_type="application/json"
        )
        article = json.loads(post_resp.data)
        aid = article["id"]

        # Mise à jour partielle (uniquement le titre)
        update_payload = {"titre": "Updated Partial Title"}
        update_resp = self.client.put(
            f"/articles/{aid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)
        updated_article = json.loads(update_resp.data)
        self.assertEqual(updated_article["titre"], "Updated Partial Title")
        self.assertEqual(updated_article["contenu"], "Initial Content")


if __name__ == "__main__":
    unittest.main()
