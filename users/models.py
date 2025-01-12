from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from os import path
from uuid import uuid4


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    user = instance.user
    full_name = user.get_full_name().replace(" ", "")
    return f"images/users/{full_name}/{new_filename}"


#====================================== CustomUserManager Model =======================================

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("وارد کردن ایمیل ضروری است.")
        
        user = self.model(
            username = username,
            first_name = first_name.capitalize(),
            last_name = last_name.capitalize(),
            email = self.normalize_email(email),
        )
        user.set_password(password)
        user.user_type = "user"
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.user_type = "backend"
        user.save(using=self._db)
        return user


#======================================= CustomUser Model ===============================================

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [("backend", "BackEnd"), ("frotend", "FrontEnd"), ("admin", "Admin"), ("premium", "Premium"), ("user", "User"), ]
    username = models.CharField(max_length=30, unique=True, verbose_name="Username")
    first_name = models.CharField(max_length=30, verbose_name="First Nmae")
    last_name = models.CharField(max_length=30, verbose_name="Last Nmae")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    user_type = models.CharField(max_length=30, choices=USER_TYPE, default="user", verbose_name="User Type")
    is_active = models.BooleanField(default=False, verbose_name="Being Active")
    is_premium = models.BooleanField(default=False, verbose_name="Being Premium")
    is_admin = models.BooleanField(default=False, verbose_name="Being Admin")
    is_superuser = models.BooleanField(default=False, verbose_name="Being Superuser")
    joined_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Joined At")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated At")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


#==================================== UserProfile Model =================================================

class UserProfile(models.Model):
    GENDER = [("male", "آقا"), ("female", "خانوم"), ("other", "نمی گویم")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="UserProfile_user", verbose_name="User")
    phone = models.CharField(max_length=12, unique=True, verbose_name="Phone Number")
    gender = models.CharField(max_length=30, choices=GENDER, default="other", verbose_name="Gender")
    address = models.TextField(verbose_name="Address")   
    bio = models.TextField(blank=True, null=True, verbose_name="Bio")
    profile_picture = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Profile Picture")


#==================================== PremiumSubscription Model =========================================

class PremiumSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name="PremiumSubscription_user", verbose_name="User")
    status = models.BooleanField(default=False, verbose_name="Status")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    

#========================================================================================================