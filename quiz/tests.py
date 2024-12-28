from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Classe, Cours
from student.models import Student
from quiz.models import Subject, Quiz, Question, Answer, TakenQuiz, StudentAnswer


class QuizModelTest(TestCase):
    def setUp(self):
        # Préparation des données nécessaires pour les tests
        self.user = User.objects.create_user(username="testuser", password="password")
        self.student_user = User.objects.create_user(username="studentuser", password="password")
        self.student = Student.objects.create(user=self.student_user)
        self.subject = Subject.objects.create(name="Mathematics", color="#FF5733")
        self.classe = Classe.objects.create(nom="Classe A", description="Terminale S")
        self.cours = Cours.objects.create(name="Algebra", classe=self.classe, description="Basic algebra course")
        self.quiz = Quiz.objects.create(
            owner=self.user,
            name="Algebra Quiz",
            subject=self.subject,
            classe=self.classe,
            cours=self.cours
        )
        self.question = Question.objects.create(quiz=self.quiz, text="What is 2 + 2?")
        self.correct_answer = Answer.objects.create(question=self.question, text="4", is_correct=True)
        self.wrong_answer = Answer.objects.create(question=self.question, text="3", is_correct=False)

    def test_subject_creation(self):
        # Vérification de la création du sujet
        self.assertEqual(str(self.subject), "Mathematics")
        self.assertIn("#FF5733", self.subject.get_html_badge())

    def test_quiz_creation(self):
        # Vérification de la création du quiz
        self.assertEqual(str(self.quiz), "Algebra Quiz")
        self.assertEqual(self.quiz.owner, self.user)

    def test_question_creation(self):
        # Vérification de la création de la question
        self.assertEqual(str(self.question), "What is 2 + 2?")

    def test_answer_creation(self):
        # Vérification de la création des réponses
        self.assertEqual(str(self.correct_answer), "4")
        self.assertTrue(self.correct_answer.is_correct)
        self.assertFalse(self.wrong_answer.is_correct)

    def test_taken_quiz(self):
        # Vérification de la participation à un quiz
        taken_quiz = TakenQuiz.objects.create(
            student=self.student,
            quiz=self.quiz,
            score=90,
            percentage=90.0
        )
        self.assertEqual(str(taken_quiz), f"{self.student_user.username} - Algebra Quiz")
        self.assertEqual(taken_quiz.score, 90)
        self.assertEqual(taken_quiz.percentage, 90.0)

    def test_student_answer(self):
        # Vérification des réponses des étudiants
        student_answer = StudentAnswer.objects.create(
            student=self.student,
            answer=self.correct_answer
        )
        self.assertEqual(str(student_answer), f"{self.student_user.username} - {self.correct_answer.text}")
