from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import *
from .serializers import *
from custom_permission import UserCheckOut
from utiles import code_generator, email_sender


#======================================== Custom User View ===========================================



#======================================= Verify Email View ===========================================



#======================================= User Profile View ===========================================



#======================================= Login View ==================================================



#======================================= Fetch Users View ============================================



#======================================= Update User View ============================================



#======================================= Forget Password View ========================================



#=====================================================================================================