from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductModel
        fields = ['name','description','price','stock']
    def create(self, validated_data):
        product = ProductModel.objects.create(**validated_data)
        return product