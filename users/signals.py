from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import *


#==================================== UpdateSubscription Model ==========================================

@receiver(post_save, sender=Payment)
def update_subscription(sender, instance, **kwargs):
    if instance.payment_status == "completed":
        instance.process_payment()


#========================================================================================================