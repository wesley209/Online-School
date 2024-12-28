from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Cours
from .models import Sujet, Reponse
from django.utils.text import slugify
import uuid


class SujetModelTest(TestCase):
    def setUp(self):
        # Création des données nécessaires
        self.user = User.objects.create_user(username="testuser", password="password")
        self.cours = Cours.objects.create(
            nom="Mathématiques", description="Cours de mathématiques avancées"
        )
        self.titre = "Problème d'équation quadratique"
        self.question = "Comment résoudre une équation quadratique avec des coefficients complexes ?"

    def test_sujet_creation(self):
        # Création d'un sujet
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            question=self.question,
            titre=self.titre,
        )
        # Vérifications
        self.assertEqual(
            sujet.user, self.user, "Le sujet doit être lié à l'utilisateur correct."
        )
        self.assertEqual(
            sujet.cours, self.cours, "Le sujet doit être lié au cours correct."
        )
        self.assertEqual(
            sujet.titre, self.titre, "Le titre du sujet doit être correct."
        )
        self.assertTrue(
            sujet.slug.startswith(slugify(self.titre)),
            "Le slug du sujet doit commencer par le titre slugifié.",
        )

    def test_sujet_str(self):
        sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            question=self.question,
            titre=self.titre,
        )
        self.assertEqual(
            str(sujet),
            self.titre,
            "La méthode __str__ du sujet doit retourner le titre.",
        )


class ReponseModelTest(TestCase):
    def setUp(self):
        # Création des données nécessaires
        self.user = User.objects.create_user(username="testuser2", password="password")
        self.cours = Cours.objects.create(
            nom="Physique", description="Cours de physique quantique"
        )
        self.sujet = Sujet.objects.create(
            user=self.user,
            cours=self.cours,
            question="Qu'est-ce que le spin en mécanique quantique ?",
            titre="Spin des particules",
        )
        self.reponse_text = (
            "Le spin est une propriété intrinsèque des particules subatomiques."
        )

    def test_reponse_creation(self):
        # Création d'une réponse
        reponse = Reponse.objects.create(
            user=self.user,
            sujet=self.sujet,
            reponse=self.reponse_text,
        )
        # Vérifications
        self.assertEqual(
            reponse.user,
            self.user,
            "La réponse doit être liée à l'utilisateur correct.",
        )
        self.assertEqual(
            reponse.sujet, self.sujet, "La réponse doit être liée au sujet correct."
        )
        self.assertEqual(
            reponse.reponse,
            self.reponse_text,
            "Le texte de la réponse doit être correct.",
        )
        self.assertTrue(
            reponse.slug.startswith(slugify(self.sujet.titre)),
            "Le slug de la réponse doit inclure le titre du sujet slugifié.",
        )

    def test_reponse_str(self):
        reponse = Reponse.objects.create(
            user=self.user,
            sujet=self.sujet,
            reponse=self.reponse_text,
        )
        self.assertEqual(
            str(reponse),
            self.sujet.titre,
            "La méthode __str__ de la réponse doit retourner le titre du sujet.",
        )
