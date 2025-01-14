from rest_framework import serializers
from .models import *
from utilities import *


# {
#     "username": "soheil-daliri",
#     "first_name": "Soheil",
#     "last_name": "Daliri",
#     "email": "the.techie.guy92@gmail.com",
#     "password": "Soheil0014@",
#     "re_password": "Soheil0014@",
#     "is_admin": "True",
#     "is_superuser": "True"
# }

#======================================= Custom User Serializer ====================================

class CustomUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=20, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password", "re_password", "is_admin", "is_superuser"]
    
    def create(self, validated_data):
        is_admin = validated_data.pop("is_admin", False)
        is_superuser = validated_data.pop("is_superuser", False)
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError("وارد کردن رمز عبور ضروری است.")
        
        user = CustomUser.objects.create_user(
            username = validated_data["username"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            email = validated_data["email"],
            password = password
        )
        
        if is_admin:
            user.is_admin = True 
        if is_superuser:
            user.is_superuser = True 
        if is_admin or is_superuser:
            user.user_type = "frontend"
        
        user.save()
        return user
    
    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError("رمز عبور و تکرار آن یکسان نمی باشد.")
        if not passwordRe.match(attrs["password"]):
            raise serializers.ValidationError("رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد.")
        return attrs
    
    def validate_email(self, attr):
        if not emailRe.match(attr):
            raise serializers.ValidationError("ایمیل معتبر نیست.")
        return attr


#======================================= User Profile Serializers ==================================

class UserProfileSerializer(serializers.ModelSerializer):
    pass


#======================================= Login Serializer ==========================================

class LoginSerializer(serializers.Serializer):
    pass


#======================================= Fetch Users Serializer ====================================

class FetchUsersSerializer(serializers.ModelSerializer):
    pass


#======================================= Update User Serializer ====================================

class UpdateUserSerializer(serializers.ModelSerializer):
    pass


#======================================= Forget Password Serializer ================================

class PasswordResetSerializer(serializers.Serializer):
    pass


class SetNewPasswordSerializer(serializers.Serializer):
    pass


#===================================================================================================
