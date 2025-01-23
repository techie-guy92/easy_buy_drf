from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from utilities import email_sender, replace_dash_to_space
from logging import getLogger


#==================================== UpdateProduct Model ===============================================

logger = getLogger(__name__)


def send_approval_email(user, product):
    try:
        verification_link = f"http://127.0.0.1:8000/product/{user.username}-{replace_dash_to_space(product)}/?next=/product/{user.username}-{replace_dash_to_space(product)}/"
        subject = "Your product has been approved"
        message = "The product you incorporated to sell has been approved."
        html_content = f"""
            <p>Hello {user.first_name} {user.last_name},<br><br>
            We're excited to let you know that your product, '{product}', has been approved! You can now check it out on Easy Buy.<br>
            <a href='{verification_link}'>Go to Easy Buy</a><br><br>
            Thank you for choosing us!</p>
        """
        email_sender(subject, message, html_content, [user.email])
        print(verification_link)
    except Exception as error:
        logger.error(f"Failed to send approval email to {user.email}: {error}")
        raise

@receiver(post_save, sender=Product)
def update_product(sender, instance, **kwargs):
    if instance.is_active:
        send_approval_email(instance.user, instance.product)


#========================================================================================================