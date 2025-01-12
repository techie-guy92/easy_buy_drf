from django.contrib import admin
from .models import *


#==================================== Category Admin ========================================

@admin.register(Category)
class  CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "parent", "slug")
    list_filter = ("parent",)
    list_search = ("category",)
    ordering = ("category",)


#==================================== Product Admin ========================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "id", "category", "slug", "price", "is_active", "willing_exchange", "created_at")
    list_filter = ("is_active",)
    list_search = ("product", "user", "id",)
    list_editable = ("is_active",)
    ordering = ("product",)


#==================================== Gallery Admin ========================================

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("gallery",)


#================================================================================================

