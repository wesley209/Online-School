from django.test import TestCase
from school.models import Matiere, Niveau, Classe, Chapitre, Cours
from datetime import date


class SchoolModelsTest(TestCase):

    def setUp(self):
        # Création d'instances pour les tests
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)
        self.matiere = Matiere.objects.create(
            nom="Mathématiques", description="Cours de maths"
        )
        self.chapitre = Chapitre.objects.create(
            classe=self.classe,
            matiere=self.matiere,
            titre="Introduction aux fonctions",
            duree_en_heure=2,
            description="Description du chapitre",
            date_debut=date(2024, 1, 10),
            date_fin=date(2024, 1, 15),
        )
        self.cours = Cours.objects.create(
            titre="Les fonctions linéaires",
            chapitre=self.chapitre,
            description="Description du cours",
        )

    def test_niveau_creation(self):
        # Test de la création d'un niveau
        self.assertEqual(str(self.niveau), "Terminale")
        self.assertTrue(self.niveau.slug.startswith("terminale-"))

    def test_classe_creation(self):
        # Test de la création d'une classe
        self.assertEqual(str(self.classe), "Terminale 1")
        self.assertEqual(self.classe.niveau, self.niveau)

    def test_matiere_creation(self):
        # Test de la création d'une matière
        self.assertEqual(str(self.matiere), "Mathématiques")
        self.assertTrue(self.matiere.slug.startswith("mathematiques-"))

    def test_chapitre_creation(self):
        # Test de la création d'un chapitre
        self.assertEqual(str(self.chapitre), "Introduction aux fonctions")
        self.assertEqual(self.chapitre.classe, self.classe)
        self.assertEqual(self.chapitre.matiere, self.matiere)
        self.assertTrue(self.chapitre.slug.startswith(
            "introduction-aux-fonctions-"))

    def test_cours_creation(self):
        # Test de la création d'un cours
        self.assertEqual(str(self.cours), "Les fonctions linéaires")
        self.assertEqual(self.cours.chapitre, self.chapitre)
        self.assertTrue(self.cours.slug.startswith("les-fonctions-lineaires-"))
