from django.test import TestCase
from rest_framework.test import APIClient

from core_auth.models import User
from course.models import Category, Course


class CourseListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title="Programming", emoji="💻")

    def _course(self, title, slug, featured=False, category=None):
        return Course.objects.create(
            title=title,
            slug=slug,
            category=category or self.category,
            featured=featured,
        )

    def test_list_is_public(self):
        self._course("Python Basics", "python-basics")
        response = self.client.get("/api/v1/course/list/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_featured_courses_come_first(self):
        self._course("Regular", "regular", featured=False)
        self._course("Featured", "featured", featured=True)

        response = self.client.get("/api/v1/course/list/")

        results = response.data["results"]
        self.assertEqual(results[0]["slug"], "featured")
        self.assertEqual(results[1]["slug"], "regular")

    def test_list_filters_by_category(self):
        other = Category.objects.create(title="Design", emoji="🎨")
        self._course("Python Basics", "python-basics")
        self._course("UI Design", "ui-design", category=other)

        response = self.client.get(f"/api/v1/course/list/{other.id}/")

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["slug"], "ui-design")

    def test_pagination_is_nine_per_page(self):
        for i in range(10):
            self._course(f"Course {i}", f"course-{i}")

        response = self.client.get("/api/v1/course/list/")

        self.assertEqual(response.data["count"], 10)
        self.assertEqual(len(response.data["results"]), 9)


class CategoryViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

    def test_category_list_is_public_and_ordered(self):
        Category.objects.create(title="Programming", emoji="💻", order=1)
        Category.objects.create(title="Design", emoji="🎨", order=0)

        response = self.client.get("/api/v1/course/cat/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["title"], "Design")

    def test_create_category_requires_admin(self):
        response = self.client.post("/api/v1/course/cat/", {"title": "Marketing"}, format="json")
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.user)
        response = self.client.post("/api/v1/course/cat/", {"title": "Marketing"}, format="json")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.superuser)
        response = self.client.post("/api/v1/course/cat/", {"title": "Marketing"}, format="json")
        self.assertEqual(response.status_code, 201)

    def test_category_detail_returns_its_courses(self):
        category = Category.objects.create(title="Programming", emoji="💻")
        Course.objects.create(title="Python Basics", slug="python-basics", category=category)
        Course.objects.create(title="Django 101", slug="django-101", category=category)

        response = self.client.get(f"/api/v1/course/cat/{category.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_delete_category_requires_admin(self):
        category = Category.objects.create(title="Programming", emoji="💻")

        self.client.force_authenticate(self.user)
        response = self.client.delete(f"/api/v1/course/cat/{category.id}/")
        self.assertEqual(response.status_code, 403)

        self.client.force_authenticate(self.superuser)
        response = self.client.delete(f"/api/v1/course/cat/{category.id}/")
        self.assertEqual(response.status_code, 204)
