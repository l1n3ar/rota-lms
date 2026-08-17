import random
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

def generate_six_digit_code():
    return str(random.SystemRandom().randint(100000, 999999))

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6, default=generate_six_digit_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        app_label = 'core_auth'
        db_table = 'auth_otp'
        indexes = [
            models.Index(fields=['code', 'user', 'is_used']),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Code expires in 5 minutes
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    @property
    def is_valid(self) -> bool:
        return not self.is_used and timezone.now() < self.expires_at