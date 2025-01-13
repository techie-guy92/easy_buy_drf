from rest_framework import serializers
from django.conf import settings
from re import compile
from .models import *
from utiles import code_generator, email_sender


#======================================= Custom User Serializer ====================================

class CustomUserSerializers(serializers.ModelSerializer):
    pass


#======================================= User Profile Serializers ==================================

class UserProfileSerializers(serializers.ModelSerializer):
    pass


#======================================= Login Serializer ==========================================

class LoginSerializers(serializers.Serializer):
    pass


#======================================= Fetch Users Serializer ====================================

class FetchUsersSerializers(serializers.ModelSerializer):
    pass


#======================================= Update User Serializer ====================================

class UpdateUserSerializers(serializers.ModelSerializer):
    pass


#======================================= Forget Password Serializer ================================

class PasswordResetSerializers(serializers.Serializer):
    pass


class SetNewPasswordSerializers(serializers.Serializer):
    pass


#===================================================================================================
