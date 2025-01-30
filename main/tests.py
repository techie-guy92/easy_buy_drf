import django
import os
django.setup()
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import resolve, reverse
from users.models import *
from main.models import *
from .urls import *
from .serializers import *
from .views import *


# Run tests using: python manage.py test
# Run tests using: python manage.py test app_name.tests_module.TestClass

#======================================== Product Add Test =========================================

#======================================== Product Add Test =========================================

#======================================== Product Add Test =========================================

#===================================================================================================
