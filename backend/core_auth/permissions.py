from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsProfileComplete(IsAuthenticated):
    """
    Blocks access to core application views if the user hasn't
    completed their progressive profiling (first_name, last_name).
    """
    message = "You must complete your profile by providing your name."

    def has_permission(self, request, view):
        # First ensure they have a valid JWT (inherits from IsAuthenticated)
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False

        # Read the state directly from the JWT payload
        # This prevents an extra database hit on every API request
        token_payload = request.auth.payload if request.auth else {}

        # Fallback to DB check if token doesn't have the claim
        return token_payload.get('profile_complete', request.user.profile_complete)


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit or delete objects.
    Normal authenticated users are restricted to viewing (GET).
    """

    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # Write permissions are only allowed to superusers
        return request.user and request.user.is_superuser
