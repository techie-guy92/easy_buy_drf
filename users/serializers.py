from rest_framework import serializers
from .models import *
from utilities import *


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


#======================================= Login Serializer ==========================================

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    
    
#======================================= User Profile Serializers ==================================

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": False}
        }


#======================================= Update User Serializer ====================================

class UpdateUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=20, write_only=True, required=False)
    
    class Meta:
        model= CustomUser
        fields = ["first_name", "last_name", "email", "password", "re_password"]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": False},
            "password": {"required": False}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate(self, attrs):
        if attrs.get("password"):
            if attrs.get("password")  != attrs.get("re_password"):
                raise serializers.ValidationError("رمز عبور و تکرار آن یکسان نمی باشد.")
            if not passwordRe.match(attrs.get("password") ):
                raise serializers.ValidationError("رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد.")
        return attrs


#======================================= Forget Password Serializer ================================

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, write_only=True)
    re_password = serializers.CharField(max_length=20, write_only=True)
    token = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")
        if password != re_password:
            raise serializers.ValidationError("رمز عبور و تکرار آن یکسان نمی باسد.")
        if not passwordRe.match(password):
            raise serializers.ValidationError("رمز عبور باید متشکل از حروف کوچک، بزرگ و عدد باشد و همچنین هشت رقم داشته باشد.")
        return attrs
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("password", None)
        data.pop("re_password", None)
        return data


#======================================= Fetch Users Serializer ====================================

class FetchUsersSerializer(serializers.ModelSerializer):
     class Meta:
         model = CustomUser
         fields = ["id", "username", "first_name", "last_name", "email", "is_active", "user_type", "joined_at"]


#===================================================================================================
