from rest_framework import serializers
from .models import *
from utilities import *


#======================================== Product Serializer =======================================

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__" 
        extra_kwargs = {
            "user": {"required": False},
            "slug": {"required": False}
        }
        

#===================================================================================================