from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProgressiveTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Bake the state into the token for stateless frontend routing
        token['email'] = user.email
        token['profile_complete'] = user.profile_complete

        return token