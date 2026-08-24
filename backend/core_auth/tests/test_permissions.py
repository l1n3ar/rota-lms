from types import SimpleNamespace
from unittest.mock import Mock

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from core_auth.models import User
from core_auth.permissions import IsProfileComplete, IsSuperUserOrReadOnly


def permission_request(method, user=None, auth=None):
    """Build a minimal request carrying just what the permissions read."""
    return SimpleNamespace(
        method=method,
        user=user if user is not None else AnonymousUser(),
        auth=auth,
    )


class IsSuperUserOrReadOnlyTests(TestCase):

    def setUp(self):
        self.permission = IsSuperUserOrReadOnly()
        self.user = User.objects.create_user(email="student@example.com")
        self.superuser = User.objects.create_user(
            email="admin@example.com",
            is_staff=True,
            is_superuser=True,
        )

    def test_anonymous_get_denied(self):
        request = permission_request("GET")
        self.assertFalse(self.permission.has_permission(request, None))

    def test_authenticated_get_allowed(self):
        request = permission_request("GET", user=self.user)
        self.assertTrue(self.permission.has_permission(request, None))

    def test_non_superuser_write_denied(self):
        request = permission_request("POST", user=self.user)
        self.assertFalse(self.permission.has_permission(request, None))

    def test_superuser_write_allowed(self):
        request = permission_request("POST", user=self.superuser)
        self.assertTrue(self.permission.has_permission(request, None))


class IsProfileCompleteTests(TestCase):

    def setUp(self):
        self.permission = IsProfileComplete()
        self.complete = User.objects.create_user(
            email="done@example.com",
            first_name="Jane",
            last_name="Doe",
        )
        self.incomplete = User.objects.create_user(email="new@example.com")

    def test_unauthenticated_denied(self):
        request = permission_request("GET")
        self.assertFalse(self.permission.has_permission(request, None))

    def test_falls_back_to_db_when_no_token(self):
        self.assertTrue(
            self.permission.has_permission(permission_request("GET", user=self.complete), None)
        )
        self.assertFalse(
            self.permission.has_permission(permission_request("GET", user=self.incomplete), None)
        )

    def test_claim_overrides_db_state(self):
        request = permission_request(
            "GET",
            user=self.incomplete,
            auth=Mock(payload={"profile_complete": True}),
        )
        self.assertTrue(self.permission.has_permission(request, None))
