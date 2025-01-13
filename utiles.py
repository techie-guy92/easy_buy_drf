from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from random import choice
from string import ascii_letters, digits


#======================================= Needed Methods =====================================

def code_generator(count):
    # characters = list(string.ascii_letters + string.digits + "!?@#$%&*")
    characters = list(ascii_letters + digits)
    code_list = [choice(characters) for _ in range(count)]
    return "".join(code_list)
    
def email_sender(subject, message, HTML_Content, to):
    sender = settings.EMAIL_HOST_USER
    message = EmailMultiAlternatives(subject, message, sender, to)
    # message = EmailMultiAlternatives(Subject, Message, Sending_From, [To])
    message.attach_alternative(HTML_Content, "text/html")
    message.send()
    
    
#============================================================================================