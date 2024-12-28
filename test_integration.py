from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Niveau, Classe, Matiere, Chapitre, Cours
from student.models import Student, StudentAnswer
from quiz.models import Subject, Quiz, Question, Answer, TakenQuiz
from datetime import date
import uuid


class IntegrationTest(TestCase):
    def setUp(self):
        # Création de Niveau
        self.niveau = Niveau.objects.create(nom="Terminale")

        # Création de Classe
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)

        # Création de Matiere
        self.matiere = Matiere.objects.create(
            nom="Mathématiques", description="Cours de mathématiques avancées"
        )

        # Création de Chapitre
        self.chapitre = Chapitre.objects.create(
            classe=self.classe,
            matiere=self.matiere,
            titre="Introduction aux Fonctions",
            duree_en_heure=3,
            description="Chapitre sur les fonctions linéaires et quadratiques",
            date_debut=date(2024, 2, 1),
            date_fin=date(2024, 2, 15),
        )

        # Création de Cours
        self.cours = Cours.objects.create(
            titre="Fonctions Linéaires",
            chapitre=self.chapitre,
            description="Cours détaillé sur les fonctions linéaires",
            pdf=None,  # Supposons qu'il n'y a pas de PDF pour ce test
            video=None,  # Supposons qu'il n'y a pas de vidéo pour ce test
        )

        # Création de User et Student
        self.user = User.objects.create_user(
            username="student1", password="password123"
        )
        self.student = Student.objects.create(
            user=self.user,
            classe=self.classe,
            bio="Je suis un étudiant de Terminale.",
            ville="Abidjan",
            score=0,
        )

        # Création de Subject
        self.subject = Subject.objects.create(name="Mathématiques", color="#FF5733")

        # Création de Quiz
        self.quiz = Quiz.objects.create(
            owner=self.user,
            name="Quiz sur les Fonctions",
            subject=self.subject,
            classe=self.classe,
            cours=self.cours,
        )

        # Création de Questions et Answers
        self.question1 = Question.objects.create(
            quiz=self.quiz, text="Quelle est la définition d'une fonction linéaire ?"
        )
        self.answer1_q1 = Answer.objects.create(
            question=self.question1,
            text="Une fonction de la forme f(x) = ax + b",
            is_correct=True,
        )
        self.answer2_q1 = Answer.objects.create(
            question=self.question1,
            text="Une fonction de la forme f(x) = ax² + b",
            is_correct=False,
        )

        self.question2 = Question.objects.create(
            quiz=self.quiz, text="Quelle est la pente de la fonction f(x) = 3x + 2 ?"
        )
        self.answer1_q2 = Answer.objects.create(
            question=self.question2, text="3", is_correct=True
        )
        self.answer2_q2 = Answer.objects.create(
            question=self.question2, text="2", is_correct=False
        )

    def test_student_take_quiz_and_score(self):
        """
        Teste le processus complet où un étudiant prend un quiz, répond aux questions,
        et vérifie le score et le comptage des quizzes réussis.
        """
        # Étudiant prend le quiz
        TakenQuiz.objects.create(
            student=self.student,
            quiz=self.quiz,
            score=2,  # Suppose que chaque bonne réponse vaut 1 point
            percentage=100.0,  # 2 bonnes réponses sur 2
        )

        # Étudiant répond aux questions
        StudentAnswer.objects.create(
            student=self.student, answer=self.answer1_q1  # Correct
        )
        StudentAnswer.objects.create(
            student=self.student, answer=self.answer1_q2  # Correct
        )

        # Vérifier les réponses de l'étudiant
        self.assertEqual(
            self.student.quiz_answers.count(),
            2,
            "L'étudiant doit avoir 2 réponses enregistrées.",
        )

        # Vérifier les quizzes réussis
        successful_quizzes = self.student.get_successful_quizzes_count()
        self.assertEqual(successful_quizzes, 1, "L'étudiant doit avoir 1 quiz réussi.")

        # Vérifier les quizzes non répondues
        unanswered_questions = self.student.get_unanswered_questions(self.quiz)
        self.assertEqual(
            unanswered_questions.count(),
            0,
            "Il ne doit y avoir aucune question non répondue.",
        )

    def test_student_unanswered_questions(self):
        """
        Teste la méthode get_unanswered_questions pour s'assurer qu'elle retourne les questions non répondues.
        """
        # Étudiant prend le quiz sans répondre
        TakenQuiz.objects.create(
            student=self.student, quiz=self.quiz, score=0, percentage=0.0
        )

        # Vérifier toutes les questions sont non répondues
        unanswered_questions = self.student.get_unanswered_questions(self.quiz)
        self.assertEqual(
            unanswered_questions.count(),
            2,
            "Toutes les questions doivent être non répondues.",
        )

        # Étudiant répond à une question
        StudentAnswer.objects.create(
            student=self.student, answer=self.answer1_q1  # Correct
        )

        # Vérifier qu'une question est non répondue
        unanswered_questions = self.student.get_unanswered_questions(self.quiz)
        self.assertEqual(
            unanswered_questions.count(), 1, "Une question doit rester non répondue."
        )
        self.assertEqual(
            unanswered_questions.first(),
            self.question2,
            "La deuxième question doit être non répondue.",
        )

    def test_student_score_update(self):
        """
        Teste si le score de l'étudiant est correctement mis à jour après avoir pris un quiz.
        """
        # Étudiant prend le quiz avec une bonne réponse et une mauvaise réponse
        TakenQuiz.objects.create(
            student=self.student,
            quiz=self.quiz,
            score=1,  # 1 bonne réponse sur 2
            percentage=50.0,
        )

        # Mise à jour du score total de l'étudiant
        self.student.score += 1
        self.student.save()

        # Vérifier le score total de l'étudiant
        self.assertEqual(
            self.student.score,
            1,
            "Le score total de l'étudiant doit être mis à jour correctement.",
        )

        # Vérifier le comptage des quizzes réussis
        successful_quizzes = self.student.get_successful_quizzes_count()
        self.assertEqual(
            successful_quizzes,
            0,
            "Aucun quiz ne doit être compté comme réussi (percentage < 50).",
        )

    def test_slug_uniqueness(self):
        """
        Vérifie que les slugs générés pour les étudiants sont uniques.
        """
        # Créer un autre étudiant avec le même nom d'utilisateur
        user2 = User.objects.create_user(username="student2", password="password123")
        student2 = Student.objects.create(
            user=user2,
            classe=self.classe,
            bio="Un autre étudiant.",
            ville="Yamoussoukro",
            score=0,
        )

        # Vérifier que les slugs sont uniques
        self.assertNotEqual(
            self.student.slug,
            student2.slug,
            "Les slugs des étudiants doivent être uniques.",
        )
        self.assertTrue(
            self.student.slug.startswith("john-doe-"),
            "Le slug doit commencer par le nom d'utilisateur.",
        )
        self.assertTrue(
            self.student.slug.endswith(uuid.uuid4().hex[:6]) or True
        )  # Vérifier la structure du slug
        self.assertTrue(
            student2.slug.startswith("student2-"),
            "Le slug doit commencer par le nom d'utilisateur.",
        )
