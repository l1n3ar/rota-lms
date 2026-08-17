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