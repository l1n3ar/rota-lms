from django.test import TestCase
from rest_framework.test import APIClient

from core_auth.models import User
from ticket.models import Ticket, Comment


class TicketAPITests(TestCase):
    """End-to-end tests for the ticket API (auth handled via force_authenticate)."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")
        self.other_user = User.objects.create_user(email="other@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

    def _create_ticket(self, user, **kwargs):
        defaults = {
            "created_by": user,
            "category": "general",
            "subject": "Test subject",
            "issue_description": "Test description",
        }
        defaults.update(kwargs)
        return Ticket.objects.create(**defaults)

    def test_create_ticket(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            "/api/v1/ticket/create/",
            {
                "category": "payment",
                "subject": "Cannot enroll",
                "issue_description": "I cannot enroll in the course.",
                "priority": "high",
            },
        )

        self.assertEqual(response.status_code, 201)
        ticket = Ticket.objects.get()
        self.assertEqual(ticket.created_by, self.user)
        self.assertTrue(ticket.ticket_id)

    def test_add_comment_to_own_ticket(self):
        """Regression: comment creation used stale `user=` lookups."""
        ticket = self._create_ticket(self.user)

        self.client.force_authenticate(self.user)
        response = self.client.post(
            f"/api/v1/ticket/{ticket.ticket_id}/comment/",
            {"text": "Any update?"},
        )

        self.assertEqual(response.status_code, 201)
        comment = Comment.objects.get()
        self.assertEqual(comment.ticket, ticket)
        self.assertEqual(comment.created_by, self.user)
        self.assertEqual(comment.text, "Any update?")

    def test_cannot_comment_on_others_ticket(self):
        ticket = self._create_ticket(self.other_user)

        self.client.force_authenticate(self.user)
        response = self.client.post(
            f"/api/v1/ticket/{ticket.ticket_id}/comment/",
            {"text": "Sneaky"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Comment.objects.count(), 0)

    def test_list_returns_only_own_tickets(self):
        own = self._create_ticket(self.user, subject="Own")
        self._create_ticket(self.other_user, subject="Other")

        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/ticket/")

        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], own.ticket_id)

    def test_superuser_sees_all_tickets(self):
        self._create_ticket(self.user)
        self._create_ticket(self.other_user)

        self.client.force_authenticate(self.superuser)
        response = self.client.get("/api/v1/ticket/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_detail_lookup_by_ticket_id(self):
        ticket = self._create_ticket(self.user)

        self.client.force_authenticate(self.user)
        response = self.client.get(f"/api/v1/ticket/{ticket.ticket_id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], ticket.ticket_id)
        self.assertEqual(response.data["subject"], ticket.subject)
