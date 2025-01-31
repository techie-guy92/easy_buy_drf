from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from .models import *
from utilities import *


#==================================== UpdateSubscription Model ==========================================

@receiver(post_save, sender=Payment)
def update_subscription(sender, instance, **kwargs):
    if instance.payment_status == "completed":
        instance.process_payment()



# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PremiumSubscription

@receiver(post_save, sender=PremiumSubscription)
def check_subscription_expiration(sender, instance, **kwargs):
    print(f"Signal triggered for subscription: {instance}")
    print(f"Current time: {timezone.now()}")
    print(f"Subscription end time: {instance.end_date}")

    if instance.is_expired():
        print(f"Subscription expired: {instance}")
        user = instance.user
        user.is_premium = False
        user.save()
        print(f"Updated user: {user.username} is_premium: {user.is_premium}")
    else:
        print(f"Subscription not expired: {instance.end_date} >= {timezone.now()}")



        
        
#========================================================================================================