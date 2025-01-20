from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from utilities import email_sender
from logging import getLogger


#==================================== UpdateProduct Model ===============================================

logger = getLogger(__name__)

def send_approval_email(user):
    try:
        verification_link = "http://127.0.0.1:8000"
        subject = "Your product has been approved"
        message = "The product you incorporate to sell has been approved."
        html_content = f"""
            <p>Hello dear {user.first_name} {user.last_name},<br><br>
            The product you incorporate to sell has been approved, you can check it out.<br>
            <a href='{verification_link}'>Go to Easy Buy</a><br><br>
            Thank you for choosing us!</p>
        """
        email_sender(subject, message, html_content, [user.email])
    except Exception as error:
        logger.error(f"Failed to send approval email to {user.email}: {error}")
        raise

@receiver(post_save, sender=Product)
def update_product(sender, instance, **kwargs):
    if instance.is_active:
        send_approval_email(instance.user)


#========================================================================================================