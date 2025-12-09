from django.urls import path
from .views import (
    GenericEmailView,
    PasswordResetView,
    ForgotPasswordView,
    EmailVerificationView,
    VerifyEmailConfirmationView,
    WelcomeEmailView,
    PasswordResetFormView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    HealthCheckView,
    PingDatabaseView
)

app_name = 'auth_service'

urlpatterns = [
    # Health check and database ping
    path('health/', HealthCheckView.as_view(), name='health'),
    path('ping/', PingDatabaseView.as_view(), name='ping-database'),

    # Email endpoints
    path('email/generic/', GenericEmailView.as_view(), name='generic-email'),
    path('email/password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('email/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('email/verification/', EmailVerificationView.as_view(), name='email-verification'),
    path('email/verify-confirmation/', VerifyEmailConfirmationView.as_view(), name='verify-confirmation'),
    path('email/welcome/', WelcomeEmailView.as_view(), name='welcome-email'),

    # Password reset flow pages
    path('password/reset-form/', PasswordResetFormView.as_view(), name='password-reset-form'),
    path('password/reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/reset-complete/', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
