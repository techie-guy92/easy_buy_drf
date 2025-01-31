from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from os import path
from uuid import uuid4


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    user = instance.user
    full_name = user.get_full_name().replace(" ", "-")
    return f"images/users/{full_name}/{new_filename}"


#====================================== CustomUserManager Model =======================================

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("وارد کردن ایمیل ضروری است.")
        user = self.model(
            username=username,
            first_name=first_name.capitalize(),
            last_name=last_name.capitalize(),
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.user_type = "user"
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.user_type = "backend"
        user.save(using=self._db)
        return user
    
    
#======================================= CustomUser Model ===============================================

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [("backend", "BackEnd"), ("frontend", "FrontEnd"), ("admin", "Admin"), ("premium", "Premium"), ("user", "User"),]
    username = models.CharField(max_length=30, unique=True, verbose_name="Username")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
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

    def __str__(self):
        return f"{self.user.username} - {self.phone}"

    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["gender"]),
        ]
        
        
#==================================== PremiumSubscription Model ==========================================

class PremiumSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="PremiumSubscription_user", verbose_name="User")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")

    def __str__(self):
        return f"{self.user.username}"

    def is_expired(self):
        return self.end_date < timezone.now()
    
    class Meta:
        verbose_name = "PremiumSubscription"
        verbose_name_plural = "PremiumSubscriptions"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["start_date"]),
            models.Index(fields=["end_date"]),
        ]
        
        
#==================================== Payment Model ======================================================

class Payment(models.Model):
    PAYMENT_STATUS = [("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments", verbose_name="User") 
    payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Payment ID")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100.00, verbose_name="Amount")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending", verbose_name="Payment Status")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment Date")

    def process_payment(self):
        if self.payment_status == "completed":
            self.user.is_premium = True
            # Use get_or_create to ensure a PremiumSubscription exists
            # First Parameter (Lookup Parameters): This is where you specify the fields you want to use for looking up an existing object. In your case, it's user=self.user.
            # Second Parameter (Defaults): The defaults parameter is a dictionary that defines default values to use when creating a new object. If the object already exists, the defaults values are ignored. If the object doesn't exist, a new one is created with these default values.
            premium_sub, created = PremiumSubscription.objects.get_or_create(user=self.user, defaults={
                'start_date': timezone.now(), 
                'end_date': timezone.now() + timedelta(days=90)}
            )
            if not created:  # If the subscription already exists, update dates
                premium_sub.start_date = timezone.now()
                premium_sub.end_date = premium_sub.start_date + timedelta(days=90)
            self.user.save()
            premium_sub.save()

    def __str__(self):
        return f"Payment {self.payment_id} for {self.user.username}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        indexes = [
            models.Index(fields=["user"]),  
            models.Index(fields=["payment_id"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["payment_date"]),
        ]
        

#========================================================================================================