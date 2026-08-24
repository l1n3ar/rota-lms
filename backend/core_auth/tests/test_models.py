from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from core_auth.models import OTP, User


class UserModelTests(TestCase):

    def test_create_user_without_password_sets_unusable_password(self):
        user = User.objects.create_user(email="student@example.com")
        self.assertFalse(user.has_usable_password())

    def test_create_user_with_password(self):
        user = User.objects.create_user(email="student@example.com", password="S3cure!pass")
        self.assertTrue(user.check_password("S3cure!pass"))

    def test_create_user_normalizes_email(self):
        # Django's normalize_email lowercases the domain only, not the local part
        user = User.objects.create_user(email="Student@Example.COM")
        self.assertEqual(user.email, "Student@example.com")

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_create_superuser_sets_flags(self):
        user = User.objects.create_superuser(email="admin@example.com", password="pw")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_profile_complete(self):
        incomplete = User.objects.create_user(email="new@example.com")
        complete = User.objects.create_user(
            email="done@example.com",
            first_name="Jane",
            last_name="Doe",
        )
        self.assertFalse(incomplete.profile_complete)
        self.assertTrue(complete.profile_complete)

    def test_str_returns_email(self):
        user = User.objects.create_user(email="student@example.com")
        self.assertEqual(str(user), "student@example.com")


class OTPModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="student@example.com")

    def test_save_sets_expiry_five_minutes_ahead(self):
        otp = OTP.objects.create(user=self.user)
        expected = timezone.now() + timedelta(minutes=5)
        self.assertLess(abs((otp.expires_at - expected).total_seconds()), 5)

    def test_code_is_six_digits(self):
        otp = OTP.objects.create(user=self.user)
        self.assertRegex(otp.code, r"^\d{6}$")

    def test_is_valid_for_fresh_code(self):
        otp = OTP.objects.create(user=self.user)
        self.assertTrue(otp.is_valid)

    def test_is_valid_false_when_used(self):
        otp = OTP.objects.create(user=self.user, is_used=True)
        self.assertFalse(otp.is_valid)

    def test_is_valid_false_when_expired(self):
        otp = OTP.objects.create(
            user=self.user,
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        self.assertFalse(otp.is_valid)
