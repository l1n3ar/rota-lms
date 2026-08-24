from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from core_auth.api.v1.serializers.token import ProgressiveTokenSerializer
from core_auth.models import OTP, User


class OTPRequestViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        # Throttle counters live in the cache, which persists across tests
        cache.clear()

    @override_settings(EMAIL_SANDBOX=True)
    @patch("core_auth.api.v1.views.otp.send_otp_email")
    def test_request_otp_creates_user_and_returns_debug_otp(self, mock_task):
        response = self.client.post(
            "/api/v1/auth/otp/request/",
            {"email": "student@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["detail"], "OTP sent successfully.")

        user = User.objects.get(email="student@example.com")
        otp = OTP.objects.get(user=user)
        self.assertEqual(response.data["_debug_otp"], otp.code)
        mock_task.enqueue.assert_called_once_with("student@example.com", otp.code)

    @patch("core_auth.api.v1.views.otp.send_otp_email")
    def test_request_otp_invalidates_previous_codes(self, mock_task):
        user = User.objects.create_user(email="student@example.com")
        OTP.objects.create(user=user)

        self.client.post(
            "/api/v1/auth/otp/request/",
            {"email": "student@example.com"},
            format="json",
        )

        self.assertEqual(OTP.objects.count(), 2)
        self.assertEqual(OTP.objects.filter(is_used=False).count(), 1)

    def test_request_otp_rejects_invalid_email(self):
        response = self.client.post("/api/v1/auth/otp/request/", {"email": "nope"}, format="json")
        self.assertEqual(response.status_code, 400)


class OTPVerifyViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        cache.clear()
        self.user = User.objects.create_user(email="student@example.com")
        self.otp = OTP.objects.create(user=self.user)

    def test_verify_returns_token_pair_and_burns_otp(self):
        response = self.client.post(
            "/api/v1/auth/otp/verify/",
            {"email": self.user.email, "code": self.otp.code},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertFalse(response.data["profile_complete"])

        self.otp.refresh_from_db()
        self.assertTrue(self.otp.is_used)

    def test_verify_rejects_wrong_code(self):
        response = self.client.post(
            "/api/v1/auth/otp/verify/",
            {"email": self.user.email, "code": "000000"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_used_otp_cannot_be_reused(self):
        self.otp.is_used = True
        self.otp.save(update_fields=["is_used"])

        response = self.client.post(
            "/api/v1/auth/otp/verify/",
            {"email": self.user.email, "code": self.otp.code},
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class TokenRefreshViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")

    def test_refresh_rotates_and_blacklists_old_token(self):
        refresh = ProgressiveTokenSerializer.get_token(self.user)

        first = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )
        self.assertEqual(first.status_code, 200)
        self.assertIn("access", first.data)
        self.assertIn("refresh", first.data)

        # The old refresh token is blacklisted after rotation
        second = self.client.post(
            "/api/v1/auth/token/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )
        self.assertEqual(second.status_code, 401)


class UserProfileViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="student@example.com")

    def test_me_requires_authentication(self):
        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(response.status_code, 401)

    def test_get_me_returns_profile_and_tokens(self):
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/v1/auth/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_patch_me_completes_profile(self):
        self.client.force_authenticate(self.user)
        response = self.client.patch(
            "/api/v1/auth/me/",
            {"first_name": "Jane", "last_name": "Doe"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertTrue(response.data["profile_complete"])
