from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.contrib.auth import get_user_model
from core_auth.api.v1.serializers.user import UserProfileUpdateSerializer, UserProfileResponseSerializer

User = get_user_model()


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    """
    Allows a user to retrieve or update their profile.
    This is the only authenticated endpoint accessible without a complete profile.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Always operate on the currently authenticated user
        return self.request.user

    def get_serializer_class(self):
        # Use different serializers for incoming data vs outgoing response
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserProfileResponseSerializer

    @extend_schema(
        tags=['Auth', 'Profile'],
        summary="Get Current User Profile",
        responses={200: UserProfileResponseSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        tags=['Auth', 'Profile'],
        summary="Update Profile (Complete Onboarding)",
        description="Submit first_name and last_name to complete onboarding. Returns a fresh JWT pair with updated claims.",
        request=UserProfileUpdateSerializer,
        responses={200: UserProfileResponseSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return self.update(request, partial=True, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Return the response using the full response serializer (includes new tokens)
        response_serializer = UserProfileResponseSerializer(instance)
        return Response(response_serializer.data)