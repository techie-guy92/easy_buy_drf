from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAddAPIView, ProductDisplayViewSet, ProductDetailViewSet


router = DefaultRouter()
router.register(r"products", ProductDisplayViewSet, basename="products")
# router.register(r"product", ProductDetailViewSet, basename="product")


urlpatterns = [
    path("product-add/", ProductAddAPIView.as_view(), name="product-add"),
    re_path(r'^product/(?P<slug>[-\w]+)/$', ProductDetailViewSet.as_view({"get": "retrieve"}), name="product"),
]


urlpatterns += router.urls