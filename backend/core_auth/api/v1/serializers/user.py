from rest_framework import serializers
from django.contrib.auth import get_user_model
from core_auth.api.v1.serializers.token import ProgressiveTokenSerializer

User = get_user_model()


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Validates first and last name updates.
    Both fields are required for the profile to be considered complete.
    """
    first_name = serializers.CharField(required=True, min_length=2, max_length=150)
    last_name = serializers.CharField(required=True, min_length=2, max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileResponseSerializer(serializers.ModelSerializer):
    """
    Formats the response, including a freshly minted token pair.
    """
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    profile_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_complete', 'refresh', 'access']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Mint ONE token pair so the returned access token always
        # belongs to the returned refresh token.
        refresh = ProgressiveTokenSerializer.get_token(instance)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data