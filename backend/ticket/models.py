import bleach
from bleach.sanitizer import ALLOWED_TAGS
from django.db import models
from core_auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from utils.validator import validate_attachment


class Ticket(models.Model):
    # Enums matching the TypeScript types
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('answered', 'Answered'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )

    ticket_id = models.CharField(max_length=8, unique=True, blank=True)

    # Renamed from 'user' -> 'created_by'
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets_created")

    # New Field
    category = models.CharField(max_length=50)

    # Renamed from 'title' -> 'subject'
    subject = models.CharField(max_length=110)

    # Included from original - TS probably fetches this in a detailed view
    issue_description = models.TextField(max_length=1000)

    # New Field
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')

    # Replaced 'completed_status' (Boolean) with 'status' (Choices)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')

    # Renamed from 'resolved_by' -> 'assignee'
    assignee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        related_name='tickets_assigned',
        null=True,
        blank=True
    )

    # Renamed 'created_date' -> 'created_at', added 'updated_at'
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Keeping this if you need a specific timestamp for when status changes to 'closed'
    resolved_date = models.DateTimeField(null=True, blank=True)

    attachment = models.FileField(
        upload_to='ticket/%Y/%m/',
        blank=True,
        validators=[validate_attachment]
    )

    def __str__(self):
        return self.subject

    @property
    def sanitized_description(self):
        return bleach.clean(self.issue_description, tags=ALLOWED_TAGS)

    def generate_ticket_id(self):
        return get_random_string(8, allowed_chars='0123456789abcdefzxyv')

    def get_absolute_url(self):
        # The detail view resolves by 'ticket_id' (no namespace on the include)
        return reverse("ticket-detail", kwargs={"ticket_id": self.ticket_id})

    def save(self, *args, **kwargs):
        # Automatically set resolved_date if status is closed
        if self.status == 'closed' and not self.resolved_date:
            from django.utils import timezone
            self.resolved_date = timezone.now()

        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()

            # Ensure uniqueness
            while Ticket.objects.filter(ticket_id=self.ticket_id).exists():
                self.ticket_id = self.generate_ticket_id()

        super().save(*args, **kwargs)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")

    # Changed user to created_by for consistency with Ticket model
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)

    # Renamed for consistency
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    attachment = models.FileField(
        upload_to='ticket/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_attachment]
    )

    @property
    def sanitized_text(self):
        return bleach.clean(self.text, tags=ALLOWED_TAGS)