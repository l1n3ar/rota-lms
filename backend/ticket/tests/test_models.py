from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from core_auth.models import User
from ticket.models import Comment, Ticket
from utils.validator import validate_attachment


class TicketModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="student@example.com")

    def _ticket(self, **kwargs):
        defaults = {
            "created_by": self.user,
            "category": "general",
            "subject": "Test subject",
            "issue_description": "Test description",
        }
        defaults.update(kwargs)
        return Ticket.objects.create(**defaults)

    def test_ticket_id_is_generated(self):
        ticket = self._ticket()
        self.assertEqual(len(ticket.ticket_id), 8)

    def test_ticket_id_is_unique(self):
        ticket_1 = self._ticket()
        ticket_2 = self._ticket()
        self.assertNotEqual(ticket_1.ticket_id, ticket_2.ticket_id)

    def test_str_returns_subject(self):
        ticket = self._ticket(subject="Billing question")
        self.assertEqual(str(ticket), "Billing question")

    def test_resolved_date_set_when_closed(self):
        ticket = self._ticket(status="closed")
        self.assertIsNotNone(ticket.resolved_date)
        self.assertLessEqual(ticket.resolved_date, timezone.now())

    def test_resolved_date_not_set_when_open(self):
        ticket = self._ticket(status="answered")
        self.assertIsNone(ticket.resolved_date)

    def test_sanitized_description_strips_scripts(self):
        ticket = self._ticket(issue_description="<script>alert(1)</script><b>Bold</b>")
        sanitized = ticket.sanitized_description
        self.assertNotIn("<script>", sanitized)
        self.assertIn("<b>", sanitized)

    def test_get_absolute_url_resolves(self):
        ticket = self._ticket()
        self.assertEqual(ticket.get_absolute_url(), f"/api/v1/ticket/{ticket.ticket_id}/")


class CommentModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="student@example.com")
        self.ticket = Ticket.objects.create(
            created_by=self.user,
            category="general",
            subject="Test subject",
            issue_description="Test description",
        )

    def test_comment_links_ticket_and_creator(self):
        comment = Comment.objects.create(ticket=self.ticket, created_by=self.user, text="Hello")
        self.assertEqual(comment.ticket, self.ticket)
        self.assertEqual(comment.created_by, self.user)

    def test_sanitized_text_strips_scripts(self):
        comment = Comment.objects.create(
            ticket=self.ticket,
            created_by=self.user,
            text="<script>x</script>Hello",
        )
        self.assertNotIn("<script>", comment.sanitized_text)
        self.assertIn("Hello", comment.sanitized_text)


class AttachmentValidatorTests(TestCase):

    def test_rejects_disallowed_extension(self):
        file = SimpleUploadedFile("evil.exe", b"MZ", content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            validate_attachment(file)

    def test_rejects_oversized_file(self):
        big = SimpleUploadedFile(
            "big.pdf",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="application/pdf",
        )
        with self.assertRaises(ValidationError):
            validate_attachment(big)

    def test_accepts_valid_file(self):
        file = SimpleUploadedFile("doc.pdf", b"content", content_type="application/pdf")
        validate_attachment(file)  # should not raise
