from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.text import slugify
from django.db import transaction
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from logging import getLogger 
from .models import *
from .serializers import *
from utilities import email_sender


#======================================== Product Add View =========================================
        
class ProductAddAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ProductSerializer,
        responses={201: ProductSerializer}
    )
    @transaction.atomic
    def post(self, request):
        """
        Allows authenticated users to add new products.
        """
        # Get the product name from request.data
        # product_name = request.data.get("product", "")
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()
            # category_name = str(product.category)
            product_name = str(product.product)
            slug = f"{request.user.username}-{product_name}-{product.id}"
            product.slug = slugify(slug, allow_unicode=True)
            product.save()
            return Response({"message": "محصول شما ثبت شد، و پس از تایید کارشناسان درج خواهد شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#======================================== Product Display View =====================================

class ProductDisplayViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions to display all products.
    This viewset supports ordering, pagination, and searching.

    URL examples:
    - Display all products: /products/
    - Display a single product by slug: /products/<slug>/

    Fields for search:
    - id
    - product
    - user
    - category
    - slug

    Permissions:
    - Access is restricted to authenticated users.
    """
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ["id", "product", "user", "category", "slug"]
    lookup_field = "slug"

    
    
#===================================================================================================
# Certainly! Adding `lookup_field = 'slug'` to your `ProductDisplayViewSet` tells Django REST Framework (DRF) to use the `slug` field instead of the default `id` field when performing lookups for single objects.

# By default, DRF viewsets use the primary key (usually `id`) to retrieve individual objects. When you specify `lookup_field = 'slug'`, DRF knows to use the `slug` field for these lookups. This is why the URL `http://127.0.0.1:8000/product-display/mehdi_abbasi-پراید-هاچبک-11/` works when you use the slug to identify the product.

# Here's a quick summary of how it works:
# - **Default Behavior**: DRF looks up objects using their primary key (`id`). For example, `http://127.0.0.1:8000/product-display/1/` would retrieve the product with `id` 1.
# - **Custom Lookup Field**: By setting `lookup_field = 'slug'`, DRF looks up objects using the `slug` field instead. So, `http://127.0.0.1:8000/product-display/mehdi_abbasi-پراید-هاچبک-11/` retrieves the product with that specific slug.

# This customization is useful when you want to use more descriptive and user-friendly URLs based on fields other than the primary key. In your case, using slugs allows you to create URLs that are meaningful and SEO-friendly, while ensuring they remain unique and valid for database lookups.

