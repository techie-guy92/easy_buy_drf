from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import (SignUpAPIView, ResendVerificationEmailAPIView, VerifyEmailAPIView)

router = DefaultRouter()

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("resend-verification-email/", ResendVerificationEmailAPIView.as_view(), name="resend-verification-email"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
]


urlpatterns += router.urls