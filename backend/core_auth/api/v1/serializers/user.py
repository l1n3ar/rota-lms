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
    Formats the response, including the newly minted tokens.
    """
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()
    profile_complete = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_complete', 'refresh', 'access']

    def get_refresh(self, obj):
        return str(ProgressiveTokenSerializer.get_token(obj))

    def get_access(self, obj):
        return str(ProgressiveTokenSerializer.get_token(obj).access_token)