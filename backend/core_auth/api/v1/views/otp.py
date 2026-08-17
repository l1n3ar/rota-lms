from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import get_user_model

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
    OpenApiTypes,
    inline_serializer,
)
from rest_framework import serializers

from core_auth.models.otp import OTP
from core_auth.api.v1.serializers.otp import OTPRequestSerializer, OTPVerifySerializer
from core_auth.api.v1.serializers.token import ProgressiveTokenSerializer
from core_auth.utils import send_otp_email

User = get_user_model()


class OTPRequestThrottle(AnonRateThrottle):
    rate = '5/min'


@extend_schema_view(
    post=extend_schema(
        tags=['Auth'],
        summary="Request a 6-digit OTP code",
        description=(
                "Sends a short-lived 6-digit OTP code to the provided email address via background worker. "
                "If `settings.DEBUG` is enabled, the code is also returned in the response body as `_debug_otp`."
        ),
        request=OTPRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="OTPRequestResponse",
                    fields={
                        "detail": serializers.CharField(default="OTP sent successfully."),
                        "_debug_otp": serializers.CharField(
                            required=False,
                            help_text="Only present when settings.DEBUG is True"
                        ),
                    },
                ),
                description="OTP successfully generated and queued for delivery.",
                examples=[
                    OpenApiExample(
                        "Production Response",
                        value={"detail": "OTP sent successfully."},
                    ),
                    OpenApiExample(
                        "Debug Response (DEBUG=True)",
                        value={
                            "detail": "OTP sent successfully.",
                            "_debug_otp": "482910",
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(description="Invalid email format."),
            429: OpenApiResponse(description="Rate limit exceeded (Max 5 requests/min)."),
        },
    )
)
class OTPRequestView(views.APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPRequestThrottle]

    def post(self, request, *args, **kwargs):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user, _ = User.objects.get_or_create(email=email)

        # Invalidate previous unused OTPs
        OTP.objects.filter(user=user, is_used=False).update(is_used=True)

        # Generate new OTP
        otp_instance = OTP.objects.create(user=user)

        # Dispatch the native Django 6.0 background task
        send_otp_email.enqueue(email, otp_instance.code)

        response_data = {"detail": "OTP sent successfully."}

        # Developer Experience (DX) Handling
        if settings.DEBUG:
            print(f"\n[DEBUG] OTP for {user.email}: {otp_instance.code}\n")
            response_data["_debug_otp"] = otp_instance.code

        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        tags=['Auth'],
        summary="Verify OTP and exchange for JWT tokens",
        description=(
                "Validates the 6-digit OTP code for a given email. On success, burns the OTP "
                "and issues a SimpleJWT access/refresh token pair. "
                "Also returns `profile_complete: false` if the user must finish onboarding."
        ),
        request=OTPVerifySerializer,
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="OTPVerifyResponse",
                    fields={
                        "refresh": serializers.CharField(),
                        "access": serializers.CharField(),
                        "profile_complete": serializers.BooleanField(
                            help_text="If false, frontend must route user to profile onboarding."
                        ),
                    },
                ),
                description="Authentication successful. Returns JWT pair and profile status.",
                examples=[
                    OpenApiExample(
                        "Returning User (Profile Complete)",
                        value={
                            "refresh": "eyJhbGciOiJIUzI1NiIsIn...",
                            "access": "eyJhbGciOiJIUzI1NiIsIn...",
                            "profile_complete": True,
                        },
                    ),
                    OpenApiExample(
                        "New User (Needs Onboarding)",
                        value={
                            "refresh": "eyJhbGciOiJIUzI1NiIsIn...",
                            "access": "eyJhbGciOiJIUzI1NiIsIn...",
                            "profile_complete": False,
                        },
                    ),
                ],
            ),
            400: OpenApiResponse(
                description="Invalid, used, or expired OTP code.",
                examples=[
                    OpenApiExample(
                        "Expired Code",
                        value={"detail": "OTP has expired."},
                    ),
                    OpenApiExample(
                        "Invalid Code",
                        value={"detail": "Invalid or expired OTP."},
                    ),
                ],
            ),
        },
    )
)
class OTPVerifyView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
            otp_instance = OTP.objects.get(user=user, code=code, is_used=False)
        except (User.DoesNotExist, OTP.DoesNotExist):
            return Response(
                {"detail": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not otp_instance.is_valid:
            return Response(
                {"detail": "OTP has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Burn the OTP
        otp_instance.is_used = True
        otp_instance.save(update_fields=['is_used'])

        # Generate the JWT Pair
        refresh = ProgressiveTokenSerializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'profile_complete': user.profile_complete
        }, status=status.HTTP_200_OK)