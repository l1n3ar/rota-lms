from django.urls import path

from .views import otp, user, token

urlpatterns = [
    path('otp/request/', otp.OTPRequestView.as_view(), name='otp-request'),
    path('otp/verify/', otp.OTPVerifyView.as_view(), name='otp-verify'),

    # Token Management
    path('token/refresh/', token.DecoratedTokenRefreshView.as_view(), name='token-refresh'),

    # Profile Management
    path('me/', user.UserProfileUpdateView.as_view(), name='user-profile'),

    # Profile & Social (Add these once views are created)
    # path('me/', user.UserProfileUpdateView.as_view(), name='user-profile'),
    # path('google/', social.GoogleLoginView.as_view(), name='google-login'),
]
