import django
import os
django.setup()
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import resolve, reverse
from model_bakery.baker import make
import pytz
from users.models import *
from main.models import *
from .urls import *
from .serializers import *
from .views import *


# Run tests using: python manage.py test
# Run tests using: python manage.py test app_name.tests_module.TestClass

#======================================== Needed chip ============================================

client = APIClient()

user_data_1 = {
    "username": "techie-guy92",
    "first_name": "Soheil",
    "last_name": "Daliri",
    "email": "soheil.dalirii@gmail.com",
    "password": "abcABC123&",
    "re_password": "abcABC123&",
    "is_active": True
}

user_data_2 = {
    "username": "sosha-parsa",
    "first_name": "Sosha",
    "last_name": "Parsa",
    "email": "the.techie.guy92@gmail.com",
    "password": "abcABC123&",
    "re_password": "abcABC123&",
    "is_active": True,
    "is_admin": True,
    "is_superuser": True
}

category_data_1 = {
    "category": "gadget",
    "slug": "gadget"
}

category_data_2 = {
    "category": "hobbies",
    "slug": "hobbies"
}

product_data_1 = {
    "product": "apple iphone 7 plus",
    "slug": "apple-phone-7plus",
    "price": 1000,
    "willing_exchange": False
}

product_data_2 = {
    "product": "پلی استیشن 5",
    "price": 1000,
    "willing_exchange": False
}


#======================================== Product Add Test =========================================

class ProductAddTest(APITestCase):
    
    def setUp(self):
        self.url = reverse("product-add")
        
        self.user_1 = CustomUser.objects.create(
            username=user_data_1["username"],
            first_name=user_data_1["first_name"],
            last_name=user_data_1["last_name"],
            email=user_data_1["email"]
        )
        self.user_1.is_active = user_data_1["is_active"]
        self.user_1.set_password(user_data_1["password"])
        self.user_1.save()
        
        self.user_2 = CustomUser.objects.create(
            username=user_data_2["username"],
            first_name=user_data_2["first_name"],
            last_name=user_data_2["last_name"],
            email=user_data_2["email"]
        )
        self.user_2.is_active = user_data_2["is_active"]
        self.user_2.is_admin = user_data_2["is_admin"]
        self.user_2.is_superuser = user_data_2["is_superuser"]
        self.user_2.set_password(user_data_2["password"])
        self.user_2.save()
        
        self.category_1 = Category.objects.create(category=category_data_1["category"], slug=category_data_1["slug"])
        self.category_2 = Category.objects.create(category=category_data_2["category"], slug=category_data_2["slug"])
        
        self.product_1 = Product.objects.create(
            user=self.user_1,
            category=self.category_1,
            product=product_data_1["product"],
            slug=product_data_1["slug"],
            price=product_data_1["price"]
        )
    
    def test_product_add_model(self):
        self.assertEqual(str(self.product_1), self.product_1.product)
        self.assertEqual(self.product_1.slug, "apple-phone-7plus")
    
    def test_product_add_serializer(self):
        serializer = ProductSerializer(self.product_1)
        serializer_data = serializer.data
        self.assertEqual(serializer_data["category"], self.category_1.id)
        self.assertEqual(serializer_data["product"], product_data_1["product"])
    
    def test_product_add_view_authenticated(self):
        client.force_authenticate(user=self.user_1)
        product_data_2["category"] = self.category_2.id
        response = client.post(self.url, product_data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "محصول شما ثبت شد، و پس از تایید کارشناسان درج خواهد شد.")
        
    def test_product_add_view_unauthenticated(self):
        response = self.client.post(self.url, product_data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_add_url(self):
        view = resolve("/product-add/")
        self.assertEqual(view.func.cls, ProductAddAPIView)


#======================================== Product Display Test =====================================

class ProductDisplayTest(APITestCase):
    
    def setUp(self):
        self.url = reverse("products-list")
        
    def test_product_display_view(self):
        pass 
    
    def test_product_display_slug_view(self):
        pass 
       
    def test_product_display_url(self):
        view = resolve("/product/")
        self.assertEqual(view.func.cls, ProductDisplayViewSet)
        

#======================================== Product Detail Test =======================================

class ProductDetailTest(APITestCase):
    
    def setUp(self):
        self.url = reverse("product")
    
    def test_product_detail_serializer(self):
        pass 
    
    def test_product_detail_view(self):
        pass 
    
    def test_product_detail_url(self):
        view = resolve("/product/")
        self.assertEqual(view.func.cls, ProductDetailViewSet)
        

#===================================================================================================
