from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema

class DecoratedTokenRefreshView(TokenRefreshView):
    """
    Custom wrapper around SimpleJWT's TokenRefreshView
    purely to add Swagger/OpenAPI tags via drf-spectacular.
    """
    @extend_schema(
        tags=['Auth', 'Token'],
        summary="Refresh JWT Token",
        description="Takes a refresh type JSON web token and returns a new access type JSON web token."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)