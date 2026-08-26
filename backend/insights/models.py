from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class QuizAttempt(models.Model):
    """
    Tracks a user's overall attempt on a specific quiz.
    Always created regardless of the `store_answers` setting in the Quiz model.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    quiz = models.ForeignKey(
        'quiz.Quiz',
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    # State and Scoring
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_passed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quiz'],
                condition=models.Q(is_completed=True),
                name='unique_completed_attempt_per_user'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.quiz.title} (Score: {self.score})"


class QuestionResponse(models.Model):
    """
    Tracks the exact answers given by the user.
    Only populated if quiz.store_answers == True.
    """
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    question = models.ForeignKey(
        'quiz.Question',
        on_delete=models.CASCADE
    )

    # JSONField allows scaling to multi-choice, text-input, or matching questions
    answer_data = models.JSONField(default=dict)

    # Data Integrity Snapshot
    is_correct = models.BooleanField(default=False)

    # Micro-analytics
    time_spent_seconds = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'question'], name='unique_question_per_attempt')
        ]
        indexes = [
            models.Index(fields=['attempt', 'is_correct']),
        ]

    def __str__(self):
        return f"Response by {self.attempt.user} to {self.question.title}"


class UserActionLog(models.Model):
    """
    A scalable, generic telemetry model to track ANY user event in the system.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action_type = models.CharField(max_length=50, db_index=True)

    # Generic relation to tie this log to ANY model in your project
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Flexible metadata (e.g., ip address, device, specific event details)
    metadata = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action_type']),
            models.Index(fields=['action_type', 'created_at']),
        ]

    def __str__(self):
        return f"{self.user} performed {self.action_type} at {self.created_at}"
