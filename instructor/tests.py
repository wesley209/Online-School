from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Classe
from instructor.models import Instructor
import uuid


class InstructorModelTest(TestCase):
    def setUp(self):
        # Création des données nécessaires
        self.user = User.objects.create_user(
            username="testinstructor", password="password"
        )
        self.classe = Classe.objects.create(
            nom="Terminale A", description="Classe Terminale Littéraire"
        )

    def test_instructor_creation(self):
        # Création d'un instructeur
        instructor = Instructor.objects.create(
            user=self.user,
            contact="0123456789",
            adresse="10 Rue des Palmiers",
            classe=self.classe,
            bio="Bio de l'instructeur",
            ville="Abidjan",
        )
        # Vérifications
        self.assertEqual(
            instructor.user,
            self.user,
            "L'instructeur doit être lié à l'utilisateur correct.",
        )
        self.assertEqual(
            instructor.classe,
            self.classe,
            "L'instructeur doit être lié à la bonne classe.",
        )
        self.assertEqual(
            instructor.contact,
            "0123456789",
            "Le contact doit être enregistré correctement.",
        )
        self.assertTrue(
            instructor.slug.startswith(slugify(self.user.username)),
            "Le slug doit être généré avec le nom d'utilisateur.",
        )
        self.assertEqual(
            instructor.ville, "Abidjan", "La ville doit être enregistrée correctement."
        )

    def test_slug_generation(self):
        # Vérification de la génération de slug unique
        instructor1 = Instructor.objects.create(
            user=self.user,
            contact="0123456789",
            adresse="10 Rue des Palmiers",
            classe=self.classe,
        )
        instructor2_user = User.objects.create_user(
            username="testinstructor2", password="password"
        )
        instructor2 = Instructor.objects.create(
            user=instructor2_user,
            contact="0987654321",
            adresse="20 Avenue des Manguiers",
            classe=self.classe,
        )
        self.assertNotEqual(
            instructor1.slug,
            instructor2.slug,
            "Les slugs doivent être uniques pour chaque instructeur.",
        )

    def test_instructor_str(self):
        # Test de la méthode __str__
        instructor = Instructor.objects.create(
            user=self.user,
            contact="0123456789",
            adresse="10 Rue des Palmiers",
            classe=self.classe,
        )
        self.assertEqual(
            str(instructor),
            self.user.username,
            "La méthode __str__ doit retourner le nom d'utilisateur.",
        )

    def test_get_u_type_property(self):
        # Test de la propriété get_u_type
        instructor = Instructor.objects.create(
            user=self.user,
            contact="0123456789",
            adresse="10 Rue des Palmiers",
            classe=self.classe,
        )
        self.assertTrue
        (
            instructor.get_u_type,
            "La propriété get_u_type doit renvoyer True si l'utilisateur est un instructeur.",
        )
