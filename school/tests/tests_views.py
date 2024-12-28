from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StudentUser, Instructor


class UserViewsTestCase(TestCase):
    def setUp(self):
        """
        Configuration initiale : Création d'utilisateurs pour les tests.
        """
        # Utilisateur étudiant
        self.student_user = User.objects.create_user(
            username="student", password="studentpass"
        )
        StudentUser.objects.create(user=self.student_user)

        # Utilisateur instructeur
        self.instructor_user = User.objects.create_user(
            username="instructor", password="instructorpass"
        )
        Instructor.objects.create(user=self.instructor_user)

        # Administrateur
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        self.client = Client()

    def test_login_student_redirect(self):
        """
        Teste la redirection après connexion d'un étudiant.
        """
        response = self.client.post(
            reverse("login"), {"username": "student",
                               "password": "studentpass"}
        )
        self.assertRedirects(response, reverse("index_student"))

    def test_login_instructor_redirect(self):
        """
        Teste la redirection après connexion d'un instructeur.
        """
        response = self.client.post(
            reverse("login"), {"username": "instructor",
                               "password": "instructorpass"}
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_admin_redirect(self):
        """
        Teste la redirection après connexion d'un administrateur.
        """
        response = self.client.post(
            reverse("login"), {"username": "admin", "password": "adminpass"}
        )
        self.assertRedirects(response, "/admin/")

    def test_login_invalid_user(self):
        """
        Teste le comportement avec un utilisateur invalide.
        """
        response = self.client.post(
            reverse("login"), {"username": "invalid",
                               "password": "invalidpass"}
        )
        self.assertContains(response, "Invalid username or password",
                            status_code=200)

    def test_signup_redirect_authenticated(self):
        """
        Teste la redirection des utilisateurs déjà
        connectés sur la page d'inscription.
        """
        self.client.login(username="student", password="studentpass")
        response = self.client.get(reverse("signup"))
        self.assertRedirects(response, reverse("index_student"))

    def test_forgot_password_redirect_authenticated(self):
        """
        Teste la redirection des utilisateurs déjà connectés
        sur la page de mot de passe oublié.
        """
        self.client.login(username="instructor", password="instructorpass")
        response = self.client.get(reverse("forgot_password"))
        self.assertRedirects(response, reverse("dashboard"))

    def test_logout(self):
        """
        Teste la déconnexion d'un utilisateur.
        """
        self.client.login(username="student", password="studentpass")
        response = self.client.get(reverse("deconnexion"))
        self.assertRedirects(response, reverse("login"))

    def test_islogin_success(self):
        """
        Teste l'API `islogin` avec des informations valides.
        """
        response = self.client.post(
            reverse("islogin"),
            {"username": "student", "password": "studentpass"},
            content_type="application/json",
        )
        self.assertJSONEqual(
            response.content,
            {
                "redirect": "index_student",
                "success": True,
                "message": "Vous êtes connectés!!!",
            },
        )

    def test_islogin_failure(self):
        """
        Teste l'API `islogin` avec des informations invalides.
        """
        response = self.client.post(
            reverse("islogin"),
            {"username": "wronguser", "password": "wrongpass"},
            content_type="application/json",
        )
        self.assertJSONEqual(
            response.content, {"success": False,
                               "message": "Identifiants incorrects."}
        )
