from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import otp, user  # , user, social


urlpatterns = [
    # OTP Flow: /api/v1/auth/otp/request/
    path('otp/request/', otp.OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', otp.OTPVerifyView.as_view(), name='otp-verify'),

    # Token Management: /api/v1/auth/token/refresh/
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', user.UserProfileUpdateView.as_view(), name='user-profile'),

    # Profile & Social (Add these once views are created)
    # path('me/', user.UserProfileUpdateView.as_view(), name='user-profile'),
    # path('google/', social.GoogleLoginView.as_view(), name='google-login'),
]