import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models

from utils.image_optimizer import ImageOptimizer

optimizer = ImageOptimizer(quality=85)


class Certificate(models.Model):
    """A certificate template (design) that admins can publish and issue to users."""

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    # Optional background template image rendered behind the PDF content
    picture = models.ImageField(upload_to="certificate/", default='', null=True, blank=True)
    draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Only process if an actual file was uploaded
        if self.picture and self.picture.name:
            # Landscape A4 template, resized while preserving aspect ratio
            self.picture = optimizer.process(self.picture, size=(1414, 1000))
        super().save(*args, **kwargs)


class IssuedCertificate(models.Model):
    """A single certificate issued to a specific user (one per certificate type)."""

    certificate = models.ForeignKey(
        Certificate, on_delete=models.CASCADE, related_name="issued_certificates"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issued_certificates"
    )
    # Optional score (0-100) the user achieved, shown on the PDF
    score = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(100)])
    # Unique public code shown on the PDF so anyone can verify authenticity
    verification_code = models.CharField(max_length=32, unique=True, editable=False, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["certificate", "user"], name="unique_certificate_per_user"
            ),
        ]

    def __str__(self):
        return f"{self.certificate.title} — {self.user}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = uuid.uuid4().hex
        super().save(*args, **kwargs)
