from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from django.db import transaction
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from logging import getLogger
from .models import *
from .serializers import *
from custom_permission import CheckOwnershipPermission
from utilities import email_sender


#======================================== email senders ============================================

logger = getLogger(__name__)


def confirm_email_address(user):
    try:
        # It generates a refresh token at first, then generates an access token.
        token = RefreshToken.for_user(user).access_token
        domain = "127.0.0.1:8000"
        verification_link = f"http://{domain}/users/verify-email?token={str(token)}"
        subject = "Verify your email"
        message = f"Click on the link to verify your email: {verification_link}"
        html_content = f"<p>Hello dear {user.first_name} {user.last_name},<br><br>Please click on the link below to verify your email address:<br><a href='{verification_link}'>Verify Email</a><br><br>Thank you!</p>"
        email_sender(subject, message, html_content, [user.email])
    except Exception as error:
        logger.error(f"Failed to send verification email to {user.email}: {error}")
        raise
    
def reset_password_email(user):
    try:
        # It generates just an access token which is good for short-term validity.
        token = AccessToken.for_user(user) 
        domain = "127.0.0.1:8000"
        verification_link = f"http://{domain}/users/set-new-password?token={str(token)}"
        subject = "Password Reset Request"
        message = f"Click on the link to reset your password: {verification_link}"
        html_content = f"<p>Hello dear {user.first_name} {user.last_name},<br><br>Please click on the link below to reset your password:<br><a href='{verification_link}'>Reset Password</a><br><br>Thank you!</p>"
        email_sender(subject, message, html_content, [user.email])
    except Exception as error:
        logger.error(f"Failed to send verification email to {user.email}: {error}")
        raise


#======================================== Sign Up View =============================================

class SignUpAPIView(APIView):
    @extend_schema(
        request=CustomUserSerializer,
        responses={201: CustomUserSerializer}
    )
    @transaction.atomic
    def post(self, request):
        """
        Handle user registration requests.
        """
        username = request.data.get("username")
        email = request.data.get("email")
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "این نام کاربری وحود دارد، نام کاربری دیگری انتخاب کنید."}, status=status.HTTP_400_BAD_REQUEST)
        elif CustomUser.objects.filter(email=email).exists():
            return Response({"error": "ایمل مورد نظر قبلا ثبت نام کرده است."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirm_email_address(user)
            return Response({"message": "اطلاعات شما ثبت شد، برای تکمیل فرایند ثبت نام به ایمیل خود بروید و ایمیل خود را تایید کنید."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
#======================================= Resend Verification Email View =============================

class ResendVerificationEmailAPIView(APIView):
    @extend_schema(
        request=None,
        responses={201: None}
    )
    def post(self, request):
        """
        Resend verification email to the user.
        """
        username = request.data.get("username")
        try:
            user = CustomUser.objects.get(username=username)
            if user.is_active:
                return Response({"message": "ایمیل شما قبلا تایید شده است."}, status=status.HTTP_200_OK)
            confirm_email_address(user)
            return Response({"message": "ایمیل تایید دوباره ارسال شد."}, status=status.HTTP_201_CREATED)
        except CustomUser.DoesNotExist:
            return Response({"error": "نام کاربری مورد نظر یافت نشد."}, status=status.HTTP_400_BAD_REQUEST)


#======================================= Verify Email View ===========================================
  
class VerifyEmailAPIView(APIView):
    @extend_schema(
        request=None,
        responses={201: None}
    )
    def get(self, request):
        """
        Verify user's email using the token provided.
        """
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
            return Response({"message": f"کاربر {user.username} قبلا تایید شده است."}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
                return Response({"error": "توکن معنبر نیست."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "توکن منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)


#======================================= Login View ==================================================

class LoginAPIView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={201: LoginSerializer}
    )
    def post(self, request):
        """
        Authenticate a user and return a token.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                token = RefreshToken.for_user(user).access_token
                return Response({"token": str(token)}, status=status.HTTP_200_OK)
            return Response({"error": "نام کاربری و یا رمز عبور اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
#======================================= User Profile View ===========================================

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request= UserProfileSerializer,
        responses= {201: UserProfileSerializer}
    )
    def post(self, request):
        """
        Add additional information to a user's account.
        """
        data = request.data.copy() 
        data["user"] = request.user.id
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "اطلاعات شما ذخیره شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#======================================= Update User View ============================================

class UpdateUserAPIView(APIView):
    permission_classes = [CheckOwnershipPermission]
    
    @extend_schema(
        request=UpdateUserSerializer,
        responses={201: UpdateUserSerializer}
    )
    def put(self, request):
        """
        Handle user information update requests.
        """
        user = request.user
        self.check_object_permissions(request, user)
        serializer = UpdateUserSerializer(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "اطلاعات شما با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#======================================= Forget Password View ========================================

class PasswordResetAPIView(APIView):
    @extend_schema(
        request=PasswordResetSerializer,
        responses={201: PasswordResetSerializer}
    )
    def post(self, request):
        """
        Handle to get user's email and send an email to change password.
        """
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
              user = CustomUser.objects.get(email=email)
              reset_password_email(user)
              return Response({"message": "ایمیل برای تغییر رمز عبور ارسال شد."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
              return Response({"error": "ایمیل وارد شده معنبر نمی باشد."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
class SetNewPasswordAPIView(APIView):
    @extend_schema(
        request=SetNewPasswordSerializer,
        responses={201: SetNewPasswordSerializer}
    )
    def post(self, request):
        """
        Verify user's email using the token provided and then make password hash.
        """
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data["token"]
            password = serializer.validated_data["password"]
            try:
                payload = AccessToken(token).payload
                user_id = payload.get("user_id")
                if not user_id:
                    return Response({"error": "توکن معتبر نیست و یا منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)
                user = CustomUser.objects.get(pk=user_id)
                user.set_password(password)
                user.save()
                return Response({"message": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "کاربر یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
            except InvalidToken:
                return Response({"error": "توکن معتبر نیست."}, status=status.HTTP_400_BAD_REQUEST)
            except TokenError:
                return Response({"error": "توکن منقضی شده است."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#======================================= Fetch Users View ============================================

class FetchUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.all().order_by("id")
    serializer_class = FetchUsersSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ["id", "username", "first_name", "last_name"]
    lookup_field = "username"


#=====================================================================================================