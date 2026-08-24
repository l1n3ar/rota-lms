from django.test import TestCase
from rest_framework.test import APIClient

from core_auth.models import User
from quiz.models import Answer, Question, Quiz


class QuizViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

        self.published = Quiz.objects.create(title="Published Quiz", draft=False)
        self.draft = Quiz.objects.create(title="Draft Quiz", draft=True)

        self.question = Question.objects.create(quiz=self.published, title="Capital of France?")
        Answer.objects.create(question=self.question, title="Paris", is_correct=True)
        Answer.objects.create(question=self.question, title="London", is_correct=False)

    def test_anonymous_cannot_list_quizzes(self):
        response = self.client.get("/api/v1/quiz/quizzes/")
        self.assertEqual(response.status_code, 401)

    def test_regular_user_sees_only_published_quizzes(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/quiz/quizzes/")

        self.assertEqual(response.status_code, 200)
        titles = [q["title"] for q in response.data["results"]]
        self.assertIn("Published Quiz", titles)
        self.assertNotIn("Draft Quiz", titles)

    def test_public_serializer_hides_correct_answers(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/quiz/quizzes/{self.published.id}/")

        self.assertEqual(response.status_code, 200)
        answers = response.data["questions"][0]["answers"]
        for answer in answers:
            self.assertNotIn("is_correct", answer)

    def test_admin_serializer_exposes_everything(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.get(f"/api/v1/quiz/quizzes/{self.published.id}/")

        self.assertEqual(response.status_code, 200)
        # AdminQuizSerializer is flat ('__all__') and includes internal flags
        self.assertIn("draft", response.data)

        answers_response = self.client.get("/api/v1/quiz/answers/")
        self.assertTrue(
            any("is_correct" in answer for answer in answers_response.data["results"])
        )

    def test_regular_user_cannot_create_quiz(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/v1/quiz/quizzes/", {"title": "Nope"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_superuser_can_create_quiz(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.post("/api/v1/quiz/quizzes/", {"title": "New Quiz"}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Quiz.objects.filter(title="New Quiz").exists())

    def test_superuser_can_delete_quiz(self):
        self.client.force_authenticate(self.superuser)
        response = self.client.delete(f"/api/v1/quiz/quizzes/{self.published.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Quiz.objects.filter(id=self.published.id).exists())


class QuestionAndAnswerViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")

        self.published = Quiz.objects.create(title="Published", draft=False)
        self.draft = Quiz.objects.create(title="Draft", draft=True)
        Question.objects.create(quiz=self.published, title="Pub Q")
        draft_question = Question.objects.create(quiz=self.draft, title="Draft Q")
        Answer.objects.create(question=draft_question, title="A1", is_correct=True)

    def test_questions_from_draft_quizzes_are_hidden(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/quiz/questions/")

        titles = [q["title"] for q in response.data["results"]]
        self.assertIn("Pub Q", titles)
        self.assertNotIn("Draft Q", titles)

    def test_answers_from_draft_quizzes_are_hidden(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/quiz/answers/")

        self.assertEqual(len(response.data["results"]), 0)
