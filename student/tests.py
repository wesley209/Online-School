from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Classe, Niveau
from quiz.models import Quiz, TakenQuiz
from student.models import Student
from datetime import datetime


class StudentModelTest(TestCase):

    def setUp(self):
        # Création d'objets nécessaires pour les tests
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)
        self.user = User.objects.create_user(
            username="john_doe", password="password123"
        )
        self.student = Student.objects.create(user=self.user, classe=self.classe)

        # Création d'un quiz pour les tests
        self.quiz1 = Quiz.objects.create(
            owner=self.user,
            name="Quiz Mathématiques",
            subject=None,  # À remplacer avec un sujet si disponible
            classe=self.classe,
        )
        self.quiz2 = Quiz.objects.create(
            owner=self.user,
            name="Quiz Physique",
            subject=None,  # À remplacer avec un sujet si disponible
            classe=self.classe,
        )

        # TakenQuiz pour le student
        self.taken_quiz = TakenQuiz.objects.create(
            student=self.student, quiz=self.quiz1, score=80, percentage=80.0
        )

    def test_student_creation(self):
        # Vérifie que le modèle Student est bien créé
        self.assertEqual(self.student.user.username, "john_doe")
        self.assertEqual(self.student.classe, self.classe)
        self.assertTrue(self.student.slug.startswith("john-doe-"))
        self.assertEqual(self.student.score, 0)

    def test_get_u_type_property(self):
        # Vérifie la propriété `get_u_type`
        self.assertTrue(self.student.get_u_type)

    def test_get_unanswered_questions(self):
        # Teste les questions non répondues
        unanswered_questions = self.student.get_unanswered_questions(self.quiz1)
        self.assertEqual(
            unanswered_questions.count(), 0
        )  # Aucun quiz/question configuré pour ce test précis

    def test_get_successful_quizzes_count(self):
        # Vérifie le comptage des quizzes réussis
        successful_quizzes_count = self.student.get_successful_quizzes_count()
        self.assertEqual(successful_quizzes_count, 1)

    def test_default_bio_and_ville(self):
        # Vérifie les valeurs par défaut
        self.assertEqual(self.student.bio, "Votre bio")
        self.assertEqual(self.student.ville, "Abobo")

    def test_photo_is_optional(self):
        # Vérifie que la photo peut être vide
        self.assertIsNone(self.student.photo)
