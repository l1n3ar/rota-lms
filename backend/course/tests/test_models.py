import io
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from course.models import Category, Course, CourseItem


def generate_dummy_image(name="test_image.jpg"):
    """Helper to generate a valid in-memory image for ImageField."""
    file_obj = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="white")
    image.save(file_obj, "JPEG")
    file_obj.seek(0)
    return SimpleUploadedFile(name, file_obj.read(), content_type="image/jpeg")


class CategoryModelTests(TestCase):

    def test_str_includes_emoji_and_title(self):
        category = Category.objects.create(title="Programming", emoji="💻")
        self.assertEqual(str(category), "💻 Programming")

    def test_title_is_unique(self):
        Category.objects.create(title="Design")
        with self.assertRaises(Exception):
            Category.objects.create(title="Design")


class CourseModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Programming", emoji="💻")

    def test_str_returns_title(self):
        course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            category=self.category,
        )
        self.assertEqual(str(course), "Python Basics")

    def test_defaults(self):
        course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            category=self.category,
        )
        self.assertEqual(course.price, 0)
        self.assertFalse(course.featured)

    @patch("course.models.optimizer.process")
    def test_save_without_image_skips_optimizer(self, mock_process):
        Course.objects.create(title="No Image", slug="no-image", category=self.category)
        mock_process.assert_not_called()

    @patch("course.models.optimizer.process")
    def test_save_with_image_optimizes(self, mock_process):
        dummy_image = generate_dummy_image()
        mock_process.return_value = dummy_image

        Course.objects.create(
            title="With Image",
            slug="with-image",
            category=self.category,
            picture=dummy_image,
        )

        mock_process.assert_called_once()
        _, kwargs = mock_process.call_args
        self.assertEqual(kwargs.get("size"), (900, 506))


class CourseItemModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Programming", emoji="💻")
        self.course = Course.objects.create(
            title="Python Basics",
            slug="python-basics",
            category=self.category,
        )

    def test_generic_foreign_key_links_to_content_object(self):
        item = CourseItem.objects.create(
            course=self.course,
            title="Lesson 1",
            content_object=self.category,
            order=1,
        )
        self.assertEqual(item.content_object, self.category)
        self.assertIn("Lesson 1", str(item))
