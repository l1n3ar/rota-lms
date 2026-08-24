from unittest.mock import patch

from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from core_auth.api.v1.serializers.otp import OTPRequestSerializer, OTPVerifySerializer
from core_auth.api.v1.serializers.token import ProgressiveTokenSerializer
from core_auth.api.v1.serializers.user import UserProfileResponseSerializer, UserProfileUpdateSerializer
from core_auth.models import User


class OTPRequestSerializerTests(TestCase):

    def test_valid_email(self):
        serializer = OTPRequestSerializer(data={"email": "student@example.com"})
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        serializer = OTPRequestSerializer(data={"email": "not-an-email"})
        self.assertFalse(serializer.is_valid())


class OTPVerifySerializerTests(TestCase):

    def test_valid_payload(self):
        serializer = OTPVerifySerializer(data={"email": "student@example.com", "code": "123456"})
        self.assertTrue(serializer.is_valid())

    def test_code_must_be_six_digits(self):
        serializer = OTPVerifySerializer(data={"email": "student@example.com", "code": "123"})
        self.assertFalse(serializer.is_valid())


class UserProfileUpdateSerializerTests(TestCase):

    def test_names_must_be_at_least_two_chars(self):
        serializer = UserProfileUpdateSerializer(data={"first_name": "J", "last_name": "Doe"})
        self.assertFalse(serializer.is_valid())

    def test_valid_names(self):
        serializer = UserProfileUpdateSerializer(data={"first_name": "Jane", "last_name": "Doe"})
        self.assertTrue(serializer.is_valid())


class UserProfileResponseSerializerTests(TestCase):

    def test_mints_a_single_token_pair(self):
        """Regression: get_refresh()/get_access() used to mint TWO separate pairs.

        The returned access token must come from the same minting as the
        returned refresh token (same iat / user_id, single minting call).
        """
        user = User.objects.create_user(
            email="student@example.com",
            first_name="Jane",
            last_name="Doe",
        )

        with patch(
            "core_auth.api.v1.serializers.user.ProgressiveTokenSerializer.get_token",
            wraps=ProgressiveTokenSerializer.get_token,
        ) as mock_mint:
            data = UserProfileResponseSerializer(user).data

        # Exactly ONE pair is minted per serialization
        self.assertEqual(mock_mint.call_count, 1)

        # Both tokens decode and share the same origin
        refresh = RefreshToken(data["refresh"])
        access = AccessToken(data["access"])
        self.assertEqual(access.payload["user_id"], refresh.payload["user_id"])
        self.assertEqual(access.payload["iat"], refresh.payload["iat"])

    def test_profile_complete_reflects_model(self):
        incomplete = User.objects.create_user(email="new@example.com")
        complete = User.objects.create_user(
            email="done@example.com",
            first_name="Jane",
            last_name="Doe",
        )

        self.assertFalse(UserProfileResponseSerializer(incomplete).data["profile_complete"])
        self.assertTrue(UserProfileResponseSerializer(complete).data["profile_complete"])
