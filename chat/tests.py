from django.test import TestCase
from django.contrib.auth.models import User
from school.models import Classe  # Importez le modèle Classe du module school
from .models import Salon, Message


class SalonModelTest(TestCase):
    def setUp(self):
        # Création d'une classe pour tester la création d'un salon
        self.classe = Classe.objects.create(niveau="Terminale", numeroClasse=1)

    def test_salon_creation_on_classe_save(self):
        # Vérifie si un Salon est automatiquement créé pour la classe
        salon = Salon.objects.filter(classe=self.classe).first()
        self.assertIsNotNone(
            salon,
            "Un Salon devrait être créé automatiquement lors de la sauvegarde d'une Classe.",
        )
        self.assertEqual(
            salon.classe, self.classe, "Le salon créé doit être lié à la bonne classe."
        )

    def test_salon_str(self):
        # Test la représentation en chaîne de caractères du modèle Salon
        salon = Salon.objects.get(classe=self.classe)
        self.assertEqual(
            str(salon), salon.nom, "Le __str__ du Salon devrait retourner son nom."
        )


class MessageModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour l'auteur du message
        self.user = User.objects.create_user(username="testuser", password="password")
        # Création d'une classe et d'un salon
        self.classe = Classe.objects.create(niveau="Licence 1 ", numeroClasse=1)
        self.salon = Salon.objects.create(nom="Test Salon", classe=self.classe)

    def test_message_creation(self):
        # Création d'un message
        message = Message.objects.create(
            auteur=self.user, message="Bonjour tout le monde !", salon=self.salon
        )
        self.assertEqual(
            message.auteur,
            self.user,
            "L'auteur du message doit correspondre à l'utilisateur.",
        )
        self.assertEqual(
            message.message,
            "Bonjour tout le monde !",
            "Le contenu du message doit être correct.",
        )
        self.assertEqual(
            message.salon, self.salon, "Le message doit être associé au bon salon."
        )

    def test_message_str(self):
        # Test la représentation en chaîne de caractères du modèle Message
        message = Message.objects.create(
            auteur=self.user, message="Un autre message de test", salon=self.salon
        )
        self.assertEqual(
            str(message),
            self.user.username,
            "Le __str__ du Message devrait retourner le nom de l'auteur.",
        )
