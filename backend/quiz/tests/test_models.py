import io
from PIL import Image
from unittest.mock import patch

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from quiz.models import Quiz, Question, Answer


def generate_dummy_image(name="test_image.jpg"):
    """
    Helper function to generate a valid dummy image file in memory.
    This prevents Django's ImageField from throwing validation errors.
    """
    file_obj = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="white")
    image.save(file_obj, "JPEG")
    file_obj.seek(0)
    return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")


class QuizModelTests(TestCase):

    def test_quiz_str(self):
        """Test the string representation of the Quiz model."""
        quiz = Quiz.objects.create(title="Python Basics")
        self.assertEqual(str(quiz), "Python Basics")

    @patch("quiz.models.optimizer.process")
    def test_quiz_save_without_image(self, mock_process):
        """Test that the optimizer is NOT called if no image is uploaded."""
        Quiz.objects.create(title="No Image Quiz")
        mock_process.assert_not_called()

    @patch("quiz.models.optimizer.process")
    def test_quiz_save_with_image(self, mock_process):
        """Test that the optimizer IS called with correct dimensions when an image is provided."""
        dummy_image = generate_dummy_image()
        # Make the mock return the dummy image so the model saves successfully
        mock_process.return_value = dummy_image

        Quiz.objects.create(title="Image Quiz", picture=dummy_image)

        self.assertTrue(mock_process.called)

        # Check that it passed the correct size constraint
        args, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("size"), (900, 506))


class QuestionModelTests(TestCase):

    def setUp(self):
        self.quiz = Quiz.objects.create(title="General Knowledge")

    def test_question_str(self):
        """Test the string representation of the Question model."""
        question = Question.objects.create(
            quiz=self.quiz,
            title="What is the capital of France?"
        )
        self.assertEqual(str(question), "What is the capital of France?")

    @patch("quiz.models.optimizer.process")
    def test_question_save_without_image(self, mock_process):
        Question.objects.create(quiz=self.quiz, title="No Image Question")
        mock_process.assert_not_called()

    @patch("quiz.models.optimizer.process")
    def test_question_save_with_image(self, mock_process):
        dummy_image = generate_dummy_image()
        mock_process.return_value = dummy_image

        Question.objects.create(
            quiz=self.quiz,
            title="Image Question",
            picture=dummy_image
        )

        self.assertTrue(mock_process.called)
        args, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("size"), (900, 506))


class AnswerModelTests(TestCase):

    def setUp(self):
        self.quiz = Quiz.objects.create(title="Geography Quiz")
        self.question = Question.objects.create(
            quiz=self.quiz,
            title="What is the capital of Japan?"
        )

    def test_answer_str(self):
        """Test the string representation of the Answer model."""
        answer = Answer.objects.create(
            question=self.question,
            title="Tokyo",
            is_correct=True
        )
        self.assertEqual(str(answer), "Tokyo")

    @patch("quiz.models.optimizer.process")
    def test_answer_save_without_image(self, mock_process):
        Answer.objects.create(
            question=self.question,
            title="Kyoto",
            is_correct=False
        )
        mock_process.assert_not_called()

    @patch("quiz.models.optimizer.process")
    def test_answer_save_with_image(self, mock_process):
        dummy_image = generate_dummy_image()
        mock_process.return_value = dummy_image

        Answer.objects.create(
            question=self.question,
            title="Tokyo",
            picture=dummy_image,
            is_correct=True
        )

        self.assertTrue(mock_process.called)
        args, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("size"), (900, 506))