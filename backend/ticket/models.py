import bleach
from bleach.sanitizer import ALLOWED_TAGS
from django.db import models
from core_auth.models import User
from django.urls import reverse
from django.utils.crypto import get_random_string
from utils.validator import validate_attachment


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket_id = models.CharField(max_length=8, unique=True, blank=True)
    title = models.CharField(max_length=110)
    issue_description = models.TextField(max_length=1000)
    completed_status = models.BooleanField(default=False)

    resolved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True},
        related_name='resolved_by',
        null=True,
        blank=True
    )

    created_date = models.DateTimeField(auto_now_add=True, null=True)
    resolved_date = models.DateTimeField(null=True, blank=True)

    attachment = models.FileField(
        upload_to='ticket/%Y/%m/',
        blank=True,
        validators=[validate_attachment]
    )

    def __str__(self):
        return self.title

    @property
    def sanitized_description(self):
        return bleach.clean(self.issue_description, tags=ALLOWED_TAGS)

    def generate_ticket_id(self):
        return get_random_string(8, allowed_chars='0123456789abcdefzxyv')

    def get_absolute_url(self):
        return reverse("ticket:ticket-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = self.generate_ticket_id()

            # Ensure uniqueness
            while Ticket.objects.filter(ticket_id=self.ticket_id).exists():
                self.ticket_id = self.generate_ticket_id()

        super().save(*args, **kwargs)


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    attachment = models.FileField(
        upload_to='ticket/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_attachment]
    )

    @property
    def sanitized_text(self):
        return bleach.clean(self.text, tags=ALLOWED_TAGS)