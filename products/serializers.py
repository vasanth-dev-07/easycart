from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductModel
        fields = '__all__'

    def validate_price(self,value):
        if value <= 0 :
            raise(serializers.ValidationError("Price Must Be Greater Than Zero"))
        return value
    def validate_stock(self,value):
        if value <= 0 :
            raise(serializers.ValidationError('Stock should be greater that 0'))
        return value
    def create(self, validated_data):
        product = ProductModel.objects.create(**validated_data)
        return product
    