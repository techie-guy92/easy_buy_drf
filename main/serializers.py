from rest_framework import serializers
from .models import *
from users.models import CustomUser, UserProfile


#======================================== Product Serializer =======================================

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" 
        extra_kwargs = {
            "user": {"required": False},
            "slug": {"required": False}
        }
        
        
#======================================== Product Detail Serializer ================================
        
class EmailField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.email

class ProductDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    # SerializerMethodField can be used to fetch and represent data from related models as well as unrelated models.
    phone = serializers.SerializerMethodField()
    email = EmailField(source="user", read_only=True)
    category = serializers.CharField(source="category.__str__", read_only=True)

    class Meta:
        model = Product
        fields = ["username", "phone", "email", "product", "category", "slug", "price", "description", "willing_exchange", "created_at", "image"]

    # def get_phone(self, obj):
    #     try:
    #         user_profile = UserProfile.objects.get(user=obj.user)
    #         return user_profile.phone
    #     except UserProfile.DoesNotExist:
    #         return None

    def get_phone(self, obj):
        user_profile = UserProfile.objects.filter(user=obj.user).first()
        return user_profile.phone if user_profile else None


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["phone"] = self.get_phone(instance)
        return representation


#===================================================================================================