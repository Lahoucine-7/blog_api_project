"""
Tests unitaires pour les endpoints utilisateur.

Ce fichier teste la création, la récupération, la mise à jour et la suppression d'un utilisateur.
"""

import json
import unittest
from src.app import app, db
from src.models import Utilisateur


class UtilisateursTestCase(unittest.TestCase):
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

    def test_create_utilisateur_valid(self):
        payload = {"nom": "Test User", "email": "test@example.com"}
        response = self.client.post(
            "/utilisateurs", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["nom"], "Test User")
        self.assertEqual(data["email"], "test@example.com")

    def test_create_utilisateur_missing_field(self):
        # Test sans email
        payload = {"nom": "User Without Email"}
        response = self.client.post(
            "/utilisateurs", data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_get_utilisateurs(self):
        users = [
            {"nom": "User1", "email": "user1@example.com"},
            {"nom": "User2", "email": "user2@example.com"},
        ]
        for user in users:
            self.client.post(
                "/utilisateurs", data=json.dumps(user), content_type="application/json"
            )
        response = self.client.get("/utilisateurs")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_get_utilisateur_not_found(self):
        response = self.client.get("/utilisateurs/9999")
        self.assertEqual(response.status_code, 404)

    def test_update_utilisateur(self):
        payload = {"nom": "Old Name", "email": "old@example.com"}
        create_resp = self.client.post(
            "/utilisateurs", data=json.dumps(payload), content_type="application/json"
        )
        utilisateur = json.loads(create_resp.data)
        uid = utilisateur["id"]

        update_payload = {"nom": "New Name", "email": "new@example.com"}
        update_resp = self.client.put(
            f"/utilisateurs/{uid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(update_resp.status_code, 200)
        updated_user = json.loads(update_resp.data)
        self.assertEqual(updated_user["nom"], "New Name")
        self.assertEqual(updated_user["email"], "new@example.com")

    def test_delete_utilisateur(self):
        payload = {"nom": "User To Delete", "email": "delete@example.com"}
        create_resp = self.client.post(
            "/utilisateurs", data=json.dumps(payload), content_type="application/json"
        )
        uid = json.loads(create_resp.data)["id"]

        delete_resp = self.client.delete(f"/utilisateurs/{uid}")
        self.assertEqual(delete_resp.status_code, 200)
        get_resp = self.client.get(f"/utilisateurs/{uid}")
        self.assertEqual(get_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
