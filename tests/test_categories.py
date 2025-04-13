"""
Tests unitaires pour les endpoints de catégories.

Ce fichier teste la création, la récupération, la mise à jour et la suppression d'une catégorie.
"""

import json
import unittest
from src.app import app, db
from src.models import Categorie


class CategoriesTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_category_valid(self):
        payload = {"nom": "Catégorie Test", "description": "Description de test"}
        response = self.client.post(
            "/categories", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["nom"], "Catégorie Test")
        self.assertEqual(data["description"], "Description de test")

    def test_create_category_missing_nom(self):
        payload = {"description": "Sans nom"}
        response = self.client.post(
            "/categories", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_categories(self):
        for i in range(2):
            payload = {"nom": f"Catégorie {i}", "description": f"Desc {i}"}
            self.client.post(
                "/categories", data=json.dumps(payload), content_type="application/json"
            )
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_category_not_found(self):
        response = self.client.get("/categories/9999")
        self.assertEqual(response.status_code, 404)

    def test_update_category(self):
        payload = {"nom": "Catégorie Initiale", "description": "Initiale"}
        create_resp = self.client.post(
            "/categories", data=json.dumps(payload), content_type="application/json"
        )
        category = json.loads(create_resp.data)
        cid = category["id"]

        update_payload = {"nom": "Catégorie Modifiée", "description": "Modifiée"}
        update_resp = self.client.put(
            f"/categories/{cid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)
        updated_cat = json.loads(update_resp.data)
        self.assertEqual(updated_cat["nom"], "Catégorie Modifiée")
        self.assertEqual(updated_cat["description"], "Modifiée")

    def test_delete_category(self):
        payload = {"nom": "Catégorie À Supprimer", "description": "À supprimer"}
        create_resp = self.client.post(
            "/categories", data=json.dumps(payload), content_type="application/json"
        )
        cid = json.loads(create_resp.data)["id"]

        delete_resp = self.client.delete(f"/categories/{cid}")
        self.assertEqual(delete_resp.status_code, 200)
        get_resp = self.client.get(f"/categories/{cid}")
        self.assertEqual(get_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
