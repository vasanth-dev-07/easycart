from django.shortcuts import render
from .models import OrderModel
from .serializer import OrderSerializer
from products.models import ProductModel
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import OrderModel,cartModel
from .serializer import OrderSerializer,CartSerializer
from products.models import ProductModel


class AddCartApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if product.stock < quantity:
            return Response({"error": "Not enough stock available."}, status=status.HTTP_400_BAD_REQUEST)

        # Update stock
        product.stock -= quantity
        product.save()

        total_price = quantity * float(product.price)

        # Save cart
        cart = cartModel.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )

        return Response({
            "message": f"Hooray {request.user.username}, product added to cart!",
            "product": product.name,
            "quantity": quantity,
            "remaining_stock": product.stock,
            "total_price": total_price
        }, status=status.HTTP_201_CREATED)


class ViewCartAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart_items = cartModel.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True, context={'request': request})  # ✅ this line is important
        return Response(serializer.data)

class OrderCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # user = serializer.validated_data['user']
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']

            # Check stock
            if product.stock < quantity:
                return Response(
                    {"error": "Not enough stock available."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update stock
            product.stock -= quantity
            product.save()

            total_price = quantity * float(product.price)

            # Save order
            order = serializer.save(user=request.user, total_price=total_price)
            username = request.user.username

            return Response(
                {
                    "message": "Hooray {username} your Order placed successfully!",
                    "order_id": order.id,
                    "product": product.name,
                    "quantity": quantity,
                    "total_price": total_price
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





