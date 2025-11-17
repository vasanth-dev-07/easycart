from rest_framework import serializers
from .models import OrderModel,cartModel
from products.models import ProductModel

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cartModel
        fields = ['product','quantity']

class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'price', 'image', 'category']

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

class CartSerializer(serializers.ModelSerializer):
    product = ProductMiniSerializer(read_only=True)

    class Meta:
        model = cartModel
        fields = ['id', 'product', 'quantity', 'total_price', 'ordered_at']

        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'