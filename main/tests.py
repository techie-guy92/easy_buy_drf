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
    "slug": "playstation-5",
    "price": 1000,
    "willing_exchange": False
}


#======================================== Product Add Test =========================================

class ProductAddTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
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
        self.client.force_authenticate(user=self.user_1)
        product_data_2["category"] = self.category_2.id
        response = self.client.post(self.url, product_data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "محصول شما ثبت شد، و پس از تایید کارشناسان درج خواهد شد.")
        
    # If we use `client` without `self` (define clinet out of class), we might accidentally use a `client` that has already been authenticated in previous tests or has some other configuration, 
	# leading to unexpected behavior like a `400 Bad Request` instead of `401 Unauthorized`.
    def test_product_add_view_unauthenticated(self):
        response = self.client.post(self.url, product_data_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_add_url(self):
        view = resolve("/product-add/")
        self.assertEqual(view.func.cls, ProductAddAPIView)


#======================================== Product Display Test =====================================

class ProductDisplayTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("products-list")
        
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
        self.product_1.is_active = True
        self.product_1.save()
        
        self.product_2 = Product.objects.create(
            user=self.user_2,
            category=self.category_2,
            product=product_data_2["product"],
            slug=product_data_2["slug"],
            price=product_data_2["price"]
        )
        self.product_2.is_active = True
        self.product_2.save()
        
    def test_product_display_view(self):
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
    
    def test_product_display_slug_view(self):
        self.client.force_authenticate(user=self.user_1)
        url = reverse("products-detail", kwargs={"slug": self.product_1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"], self.product_1.product)
        
    def test_product_display_url(self):
        view = resolve("/products/")
        self.assertEqual(view.func.cls, ProductDisplayViewSet)
        

#======================================== Product Detail Test =======================================

class ProductDetailTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("product", kwargs={"slug": "apple-phone-7plus"})
        
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
        self.user_2.is_premium = True
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
        self.product_1.is_active = True
        self.product_1.save()
        
        self.product_2 = Product.objects.create(
            user=self.user_2,
            category=self.category_2,
            product=product_data_2["product"],
            slug=product_data_2["slug"],
            price=product_data_2["price"]
        )
        self.product_2.is_active = True
        self.product_2.save()
    
    def test_product_detail_serializer(self):
        serializer = ProductDetailSerializer(self.product_1)
        serializer_data = serializer.data
        self.assertEqual(serializer_data["slug"], self.product_1.slug)
        self.assertIn("username", serializer_data)
        self.assertIn("email", serializer_data)

    def test_product_detail_view(self):
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"], self.product_1.product)
    
    def test_product_detail_url(self):
        view = resolve("/product/apple-phone-7plus/")
        self.assertEqual(view.func.cls, ProductDetailViewSet)
        

#===================================================================================================
