from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAddAPIView, ProductDisplayViewSet

router = DefaultRouter()
# router.register(r"product-add", ProductAddAPIView, basename="product-add")
router.register(r"product", ProductDisplayViewSet, basename="product")


urlpatterns = [
    path("product-add/", ProductAddAPIView.as_view(), name="product-add")
]


urlpatterns += router.urls