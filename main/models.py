from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from os import path
from uuid import uuid4
from users.models import *


#======================================= Needed Method ======================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4() } {ext}"
    try:
        model = getattr(instance, "category", None) or getattr(instance, "product", None) or getattr(instance, "gallery", "deafult_gallery") 
        if isinstance(instance, Category):
            return f"images/categories/{model}/{new_filename}"
        elif isinstance(instance, Product):
            return f"images/products/{model}/{new_filename}"
        else:
            return f"images/galleries/{model}/{new_filename}"
    except AttributeError:
        return f"images/others/{new_filename}"
    

#======================================= Category Model =====================================================

class Category(models.Model):
    category =models.CharField(max_length=100, verbose_name="Category")
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="Category_parent", blank=True, null=True, verbose_name="Parent")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image= models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    
    def category_name(self):
        category_part_1,  category_part_2= self.category.split("-")
        return category_part_1
      
    def __str__(self):
        return self.category_name()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["slug"]),
        ]
    

#======================================= Product Model ======================================================

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Product_user", verbose_name="User")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Product_category", verbose_name="Category")
    product = models.CharField(max_length=100, verbose_name="Product")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    price = models.PositiveIntegerField(default=0, verbose_name="Price")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=False, verbose_name="Being Active")
    willing_exchange = models.BooleanField(default=False, verbose_name="Willing Exchange")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated At")
    
    def __str__(self):
        return self.product
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["category"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["price"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["willing_exchange"]),
        ]


#======================================= Gallery Model ======================================================

class Gallery(models.Model):
    gallery = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="Gallery_gallery", verbose_name="Product")
    image = models.ImageField(upload_to=upload_to, blank=True, null=True, verbose_name="Image")
    
    def __str__(self):
        return self.gallery
    
    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"


#============================================================================================================