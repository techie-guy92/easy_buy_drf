import django
import os
django.setup()
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import jwt
from django.urls import resolve, reverse
from django.contrib.auth import authenticate
from django.core import mail
from unittest.mock import patch
from .models import *
from .urls import *
from .serializers import *
from .views import *


# Run tests using: python manage.py test
# Run tests using: python manage.py test app_name.tests_module.TestClass

#======================================== Needed chip ============================================

client = APIClient()

user_data_1 = {
    "username": "techie-guy92",
    "first_name": "Soheil",
    "last_name": "Daliri",
    "email": "soheil.dalirii@gmail.com",
    "password": "abcABC123&",
    "re_password": "abcABC123&"
}

user_data_2 = {
    "username": "sosha-parsa",
    "first_name": "Sosha",
    "last_name": "Parsa",
    "email": "the.techie.guy92@gmail.com",
    "password": "abcABC123&",
    "re_password": "abcABC123&",
    "is_admin": True,
    "is_superuser": True
}


#======================================== Sign Up Test ============================================

class SignUpTest(TestCase):
    
    def setUp(self):
        self.url = reverse("signup")
        
    def test_customeuser_model(self):
        user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
        )
        user_1.set_password(user_data_1["password"])
        user_1.save()
        self.assertEqual(str(user_1), user_1.username)
        self.assertEqual(user_1.username, user_data_1["username"])
        self.assertEqual(user_1.get_full_name(), f"{user_data_1['first_name']} {user_data_1['last_name']}")
        self.assertEqual(user_1.email, user_data_1["email"])
        self.assertEqual(user_1.user_type, "user") 
        self.assertFalse(user_1.is_active)
        self.assertFalse(user_1.is_premium)

    def test_customuser_serializer(self):
        user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
        )
        user_1.set_password(user_data_1["password"])
        user_1.save()
        serializer = CustomUserSerializer(user_1)
        serializer_data = serializer.data
        self.assertEqual(serializer_data["username"], user_data_1["username"])
        self.assertEqual(serializer_data["first_name"], user_data_1["first_name"])
        self.assertEqual(serializer_data["last_name"], user_data_1["last_name"])
        self.assertEqual(serializer_data["email"], user_data_1["email"])
        self.assertFalse(serializer_data["is_admin"])
        self.assertFalse(serializer_data["is_superuser"])
        self.assertIn("username", serializer_data)  # checks fields of serializer
        self.assertIn("email", serializer_data)
        self.assertIn("first_name", serializer_data)
        self.assertIn("last_name", serializer_data)
        self.assertIn("is_admin", serializer_data)
        self.assertIn("is_superuser", serializer_data)
    
    def test_sign_up_view(self):
        response = client.post(self.url, user_data_1, format="json")
        user = CustomUser.objects.get(username=user_data_1["username"])
        
        if response.status_code != status.HTTP_201_CREATED:
            print("Response Data: ", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "اطلاعات شما ثبت شد، برای تکمیل فرایند ثبت نام به ایمیل خود بروید و ایمیل خود را تایید کنید.")
        self.assertEqual(user.email, user_data_1["email"])
        self.assertTrue(user.check_password(user_data_1["password"]))
        self.assertEqual(len(mail.outbox), 1)  # Check that one email was sent
        self.assertEqual(mail.outbox[0].to, [user_data_1["email"]])  # Check the recipient
        self.assertIn("Verify your email", mail.outbox[0].subject)  # Check the subject
        self.assertIn("Click on the link to verify your email", mail.outbox[0].body)  # Check the email body
    
    def test_sign_up_url(self):
        view = resolve("/users/signup/")
        self.assertEqual(view.func.cls, SignUpAPIView)


#======================================== Resend Verification Email Test ==============================

class ResendVerificationEmailTest(TestCase):
    
    def setUp(self):
        self.url = reverse("resend-verification-email")
        
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        self.valid_email_data = {"username": self.user_1.username}
        self.invalid_email_data = {"username": "nonexistent@example.com"}
    
    @patch("users.views.confirm_email_address")
    def test_resend_verification_email_view(self, mock_confirm_email_address):
        response = client.post(self.url, self.valid_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "ایمیل تایید دوباره ارسال شد.")
        mock_confirm_email_address.assert_called_once_with(self.user_1)
    
    def test_already_verified_view(self):
        self.user_1.is_active = True
        self.user_1.save()
        response = client.post(self.url, self.valid_email_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "ایمیل شما قبلا تایید شده است.")
        
    def test_email_not_found_view(self):
        response = client.post(self.url, self.invalid_email_data, format="json")
        if response.status_code != status.HTTP_404_NOT_FOUND:
            print("Response Data: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "نام کاربری مورد نظر یافت نشد.")
    
    def test_resend_verification_email_url(self):
        view = resolve("/users/resend-verification-email/")
        self.assertEqual(view.func.cls, ResendVerificationEmailAPIView)


#======================================== Verify Email Test =======================================

class VerifyEmailTest(TestCase):
    
    def setUp(self):
        self.url = reverse("verify-email")
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"]
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        self.token_1 = str(RefreshToken.for_user(self.user_1).access_token) 
        self.token_2 = str(AccessToken.for_user(self.user_1))

    def test_verify_email_view(self):
        response = client.get(self.url, {"token": self.token_1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "ثبت نام شما کامل شد.")
        
    def test_already_verified_view(self):
        self.user_1.is_active = True
        self.user_1.save()
        response = client.get(self.url, {"token": self.token_1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["message"], f"کاربر {self.user_1.username} قبلا تایید شده است.")
    
    def test_verify_email_url(self):
        view = resolve("/users/verify-email/")
        self.assertEqual(view.func.cls, VerifyEmailAPIView)
    
    
#======================================== Login Test ================================================

class LoginTest(TestCase):
    
    def setUp(self):
        self.url = reverse("login")
        
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
            is_active=True 
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()

        self.login_data = {
            "username": user_data_1["username"],
            "password": user_data_1["password"]
        }
    
    def test_login_serializer(self):
        serializer = LoginSerializer(data=self.login_data)
        serializer.is_valid()
        serializer_data = serializer.data
        self.assertIn("username", serializer_data)
        self.assertNotIn("password", serializer_data) 
    
    def test_login_view(self):
        response = client.post(self.url, self.login_data, format="json")
        if response.status_code != status.HTTP_200_OK:
            print("Response Data: ", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        decoded_token = jwt.decode(response.data["token"], settings.SECRET_KEY, algorithms=["HS256"])
        self.assertEqual(decoded_token["user_id"], self.user_1.id)
        
    def test_invalid_login_view(self):
        login_data = {
            "username": user_data_1["username"],
            "password": "wrong_password"
        }
        response = client.post(self.url, login_data, format="json")
        
        if response.status_code != status.HTTP_400_BAD_REQUEST:
            print("Response Data: ", response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "نام کاربری و یا رمز عبور اشتباه است.")
        
    def test_login_url(self):
        view = resolve("/users/login/")
        self.assertEqual(view.func.cls, LoginAPIView)

        
#======================================== User Profile Test =========================================

class UserProfileTest(TestCase):
    
    def setUp(self):
        self.url = reverse("user-profile")
        
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
            is_active=True 
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        
        client.force_authenticate(user=self.user_1)
        
        self.user_profile_data = {
            "user": self.user_1.id,  
            "phone": "09123469239",
            "address": "Tehran",
            "gender": "other",
            "bio": "I'm a full-stack developer"
        }
        
    def test_user_profile_model(self):
        profile_data = UserProfile.objects.create(
            user=self.user_1,
            phone=self.user_profile_data["phone"],
            address=self.user_profile_data["address"],
            gender=self.user_profile_data["gender"],
            bio=self.user_profile_data["bio"]
        )
        self.assertEqual(str(profile_data), f"{profile_data.user.username} - {profile_data.phone}")
        
    def test_user_profile_serializer(self):
        profile_data = UserProfile.objects.create(
            user=self.user_1,
            phone=self.user_profile_data["phone"],
            address=self.user_profile_data["address"],
            gender=self.user_profile_data["gender"],
            bio=self.user_profile_data["bio"]
        )
        serializer = UserProfileSerializer(profile_data)
        serializer_data = serializer.data
        self.assertEqual(serializer_data["id"], profile_data.id)
        self.assertIn("phone", serializer_data)
        
    def test_user_profile_view(self):
        response = client.post(self.url, self.user_profile_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "اطلاعات شما ذخیره شد.")
        
    def test_user_profile_url(self):
        view = resolve("/users/user-profile/")
        self.assertEqual(view.func.cls, UserProfileAPIView)

        
#======================================== Update User Test =========================================

class UpdateUserTest(TestCase):
    
    def setUp(self):
        self.url = reverse("update-user")
        
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
            is_active=True
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        
        client.force_authenticate(user=self.user_1)
        
        self.user_2 = {
            "first_name": user_data_2["first_name"], 
            "last_name": user_data_2["last_name"],
            }
        
    def test_update_user_serializer(self):
        serializer = UpdateUserSerializer(self.user_1, data=self.user_2, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        serializer_data = serializer.data
        self.assertEqual(serializer_data["first_name"], self.user_2["first_name"])
        self.assertIn("last_name", self.user_2)
        self.assertNotIn("email", self.user_2)
    
    def test_update_user_view(self):
        response = client.put(self.url, self.user_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "اطلاعات شما با موفقیت تغییر کرد.")
        
    def test_update_user_url(self):
        view = resolve("/users/update-user/")
        self.assertEqual(view.func.cls, UpdateUserAPIView)


#======================================== Password Reset Test ======================================

class PasswordResetTest(TestCase):
    
    def setUp(self):
        self.url = reverse("password-reset")
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
            is_active=True
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        
        client.force_authenticate(user=self.user_1)
        
        self.user_2 = {"email": user_data_1["email"]}
        self.invalid_user = {"email": "invalid.email@example.com"}
        
    def test_update_user_serializer(self):
        serializer = PasswordResetSerializer(data=self.user_2)
        self.assertTrue(serializer.is_valid())
        serializer_data = serializer.data
        self.assertIn("email", serializer_data)
    
    @patch("users.views.reset_password_email")
    def test_update_valid_user_view(self, mock_reset_password_email):
        response = client.post(self.url, self.user_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "ایمیل برای تغییر رمز عبور ارسال شد.")
        mock_reset_password_email.assert_called_once_with(self.user_1)
        
    def test_update_invalid_user_view(self):
        response = client.post(self.url, self.invalid_user , format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "ایمیل وارد شده معنبر نمی باشد.")
        
    def test_password_reset_url(self):
        view = resolve("/users/password-reset/")
        self.assertEqual(view.func.cls, PasswordResetAPIView)


#======================================== Set New Password Test ====================================

class SetNewPasswordTest(TestCase):
    
    def setUp(self):
        self.url = reverse("set-new-password")
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"],
            is_active=True
        )
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        
        client.force_authenticate(user=self.user_1)
        
        self.token_1 = str(RefreshToken.for_user(self.user_1).access_token)
        self.token_2 = str(AccessToken.for_user(self.user_1))
        
        self.data = {
            "password": "abcABC123@",
            "re_password": "abcABC123@",
            "token": self.token_2
            }
        
        self.invalid_user_data = {
            "password": "abcABC123", 
            "re_password": "abcABC123", 
            "token": "invalid_token"
        }
        
    def test_set_new_password_serializer(self):
        serializer = SetNewPasswordSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        serializer_data = serializer.validated_data
        self.assertIn("password", serializer_data)
        self.assertIn("re_password", serializer_data)
        self.assertIn("token", serializer_data)
        self.assertEqual(serializer_data["password"], self.data["password"])

    
    def test_set_new_password_view(self):
        response = client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "رمز عبور با موفقیت تغییر کرد.")
        
    def test_set_new_password_invalid_data_view(self):
        response = client.post(self.url, self.invalid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.data["error"], "توکن منقضی شده است.")
        self.assertEqual(
            response.data["non_field_errors"][0],
            "رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد."
        )
        
    def test_set_new_password_url(self):
        view = resolve("/users/set-new-password/")
        self.assertEqual(view.func.cls, SetNewPasswordAPIView)


#======================================== Fetch Users Test =========================================

class FetchUsersTest(TestCase):
    
    def setUp(self):
        self.url = reverse("fetch-users-list")
        
        self.user_2 = CustomUser.objects.create(
            username=user_data_2["username"],
            first_name=user_data_2["first_name"],
            last_name=user_data_2["last_name"],
            email=user_data_2["email"],
            is_active=True, 
            is_admin=True, 
            is_superuser=True
        )
        self.user_2.set_password(user_data_2["password"])
        self.user_2.save()
        
        client.force_authenticate(user=self.user_2)
    
    def test_fetch_users_serializer(self):
        serializer = FetchUsersSerializer(self.user_2)
        serializer_data = serializer.data
        self.assertIn("username", serializer_data)
        self.assertIn("is_active", serializer_data)
    
    def test_fetch_users_view(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data.get("results", [])
        if results:
            user_data = results[0]
            self.assertEqual(user_data["email"], self.user_2.email)
            self.assertTrue(user_data["is_active"])
        else:
            self.fail("No results found in response data")
    
    def test_fetch_users_url(self):
        view = resolve("/users/fetch-users/")
        self.assertEqual(view.func.cls, FetchUsersViewSet)
  

#===================================================================================================