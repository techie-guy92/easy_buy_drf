from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from re import compile
from random import choice
from string import ascii_letters, digits
from django.utils.text import slugify


#======================================= Needed Methods =====================================

passwordRe = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*]).{8,}$")
emailRe = compile(r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$")


def code_generator(count):
    # characters = list(string.ascii_letters + string.digits + "!?@#$%&*")
    characters = list(ascii_letters + digits)
    code_list = [choice(characters) for _ in range(count)]
    return "".join(code_list)
    
    
def email_sender(subject, message, HTML_Content, to):
    sender = settings.EMAIL_HOST_USER
    message = EmailMultiAlternatives(subject, message, sender, to)
    message.attach_alternative(HTML_Content, "text/html")
    message.send()
    
    
def replace_dash_to_space(title):
        new_title="".join([eliminator.replace(" ","-") for eliminator in title])
        return new_title.lower()
    
    
#============================================================================================