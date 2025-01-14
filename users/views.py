from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import *
from .serializers import *
from custom_permission import UserCheckOut
from utilities import code_generator, email_sender


#======================================== Custom User View ===========================================

class SignUpAPIView(APIView):
    @extend_schema(
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer}
    )
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "این نام کاربری وحود دارد، نام کاربری دیگری انتخاب کنید."}, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(email=email).exists():
            return Response({"error": "ایمل مورد نظر قبلا ثبت نام کرده است."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user).access_token
            domain = "127.0.0.1:8000"
            verification_link = f"http://{domain}/users/verify-email?token={str(token)}"
            subject = "Verify your email"
            message = f"Click on the link to verify your email: {verification_link}"
            html_content = f"<p>Hello dear {user.first_name} {user.last_name}<br><br></p>Click on the link to verify your email address: <a href='{verification_link}'>Verify Email</a>"
            email_sender(subject, message, html_content, [user.email])
            return Response({"message": "اطلاعات شما ثبت شد، برای تکمیل فرایند ثبت نام به ایمیل خود بروید و ایمل خود را تایید کنید."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
#======================================= Verify Email View ===========================================

class ResendVerificationEmailAPIView(APIView):
    @extend_schema(
        request=None,
        responses={201: None}
    )
    def post(self, request):
        username = request.data.get("username")
        try:
            user = CustomUser.objects.get(username=username)
            if user.is_active:
                return Response({"message": "ایمیل شما قبلا تایید شده است."}, status=status.HTTP_200_OK)
            token = RefreshToken.for_user(user).access_token
            domain = "127.0.0.1:8000"
            verification_link = f"http://{domain}/users/verify-email?token={str(token)}"
            subject = "Verify your email"
            message = f"Click on the link to verify your email: {verification_link}"
            html_content = f"<p>Hello dear {user.first_name} {user.last_name}<br><br></p>Click on the link to verify your email address: <a href='{verification_link}'>Verify Email</a>"
            email_sender(subject, message, html_content, [user.email])
            return Response({"message": "ایمیل تایید دوباره ارسال شد."}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({"error": "نام کاربری مورد نظر یافت نشد."}, status=status.HTTP_400_BAD_REQUEST)

  
class VerifyEmailAPIView(APIView):
    @extend_schema(
        request=None,
        responses={201: None}
    )
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = AccessToken(token).payload
            user_id = payload.get("user_id")
            if not user_id:
                return Response({"error": "توکن معتبر نیست یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                return Response({"error": "کاربر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({"message": "ثبت نام شما کامل شد."}, status=status.HTTP_200_OK)
            return Response({"message": "کاربر قبلا تایید شده است."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "توکن معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)

        
#======================================= User Profile View ===========================================



#======================================= Login View ==================================================



#======================================= Fetch Users View ============================================



#======================================= Update User View ============================================



#======================================= Forget Password View ========================================



#=====================================================================================================