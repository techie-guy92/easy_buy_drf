from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from utilities import *


#==================================== UpdateSubscription Model ==========================================

@receiver(post_save, sender=Payment)
def update_subscription(sender, instance, **kwargs):
    if instance.payment_status == "completed":
        instance.process_payment()


#========================================================================================================