from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Sujet
from .views import forum
from datetime import datetime


class ForumViewTests(TestCase):
    def setUp(self):
        # Créer des objets Sujet pour les tests
        for i in range(10):
            Sujet.objects.create(
                titre=f"Sujet Général {i+1}",
                cours=None,  # Sujet général (pas lié à un cours)
                date_add=datetime.now(),
            )
        for i in range(8):
            Sujet.objects.create(
                titre=f"Sujet Lesson {i+1}",
                cours="Cours Example",  # Sujet lié à un cours
                date_add=datetime.now(),
            )

        # Instancier RequestFactory pour simuler des requêtes
        self.factory = RequestFactory()

    def test_forum_view_general_pagination(self):
        """Test que la pagination pour forum_general
        fonctionne correctement."""
        request = self.factory.get(reverse("forum") + "?page_g=1")
        response = forum(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fixed-student-forum.html")

        # Vérifie que le contexte contient la pagination correcte
        forum_general = response.context_data["forum_general"]
        self.assertEqual(forum_general.paginator.num_pages, 2)
        self.assertEqual(len(forum_general), 5)

    def test_forum_view_lessons_pagination(self):
        """Test que la pagination pour forum_lessons
        fonctionne correctement."""
        request = self.factory.get(reverse("forum") + "?page_l=1")
        response = forum(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "fixed-student-forum.html")

        # Vérifie que le contexte contient la pagination correcte
        forum_lessons = response.context_data["forum"]
        self.assertEqual(forum_lessons.paginator.num_pages, 2)
        self.assertEqual(len(forum_lessons), 5)

    def test_forum_view_invalid_page(self):
        """Test pour une page invalide."""
        request = self.factory.get(
            reverse("forum") + "?page_g=999"
        )  # Simule une page inexistante
        response = forum(request)

        self.assertEqual(response.status_code, 200)

        # Vérifie que la page par défaut est retournée
        forum_general = response.context_data["forum_general"]
        self.assertEqual(len(forum_general), 5)  # Page 1 par défaut

    def test_forum_view_no_sujets(self):
        """Test pour le cas où aucun sujet n'existe."""
        Sujet.objects.all().delete()  # Supprime tous les sujets
        request = self.factory.get(reverse("forum"))
        response = forum(request)

        self.assertEqual(response.status_code, 200)

        # Vérifie que les objets paginés sont vides
        forum_general = response.context_data["forum_general"]
        forum_lessons = response.context_data["forum"]
        self.assertEqual(len(forum_general), 0)
        self.assertEqual(len(forum_lessons), 0)