from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django.utils.text import slugify
from django.db import transaction
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from custom_permission import IsPremiumOrOwnerPermission


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
            slug = f"{request.user.username}-{product_name}"
            product.slug = slugify(slug, allow_unicode=True)
            product.save()
            return Response({"message": "محصول شما ثبت شد، و پس از تایید کارشناسان درج خواهد شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#======================================== Product Display View =====================================

class ProductDisplayViewSet(viewsets.ReadOnlyModelViewSet):
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
    
    Methods:
        get_queryset():
            Filters the initial queryset to only include active products.
    """
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ["id", "product", "user", "category", "slug"]
    # By default, viewsets use the primary key (id) to retrieve individual objects. 
    # When it specifies `lookup_field = 'slug'`, DRF knows to use the `slug` field for these lookups.
    lookup_field = "slug"
    
    def get_queryset(self):
        return self.queryset.filter(is_active=True)   


#======================================== Product Detail View =======================================

class ProductDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset that provides the detailed view of a product.

    Attributes:
        permission_classes: Only premium users can access this viewset.
        serializer_class: The serializer class used to represent the product details and seller information.
        lookup_field: The field used to look up a product by its slug.

    URL examples:
    - Display a single product by slug: /product/<slug>/
    - This viewset displays a single product, not a list of products. 

    Methods:
        get_queryset():
            Filters the initial queryset to only include active products.
    """
    permission_classes = [IsPremiumOrOwnerPermission]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# class ProductDetailAPIView(APIView):
#     """
#     View to retrieve a detailed view of a product.
    
#     Attributes:
#         permission_classes: List of permission classes for the view.

#     URL examples:
#     - Display a single product by slug: /product/<slug>/
    
#     Methods:
#         get():
#             Retrieves a single active product by its slug.
#     """
#     permission_classes = [IsAuthenticated, UserCheckOutPremium]

#     def get(self, request, slug):
#         product = get_object_or_404(Product.objects.filter(is_active=True), slug=slug)
#         self.check_object_permissions(request, product)
#         serializer = ProductDetailSerializer(product)
#         return Response(serializer.data)


#===================================================================================================