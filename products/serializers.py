from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("Stock must be greater than 0")
        return value
