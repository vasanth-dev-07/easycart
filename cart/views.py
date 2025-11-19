from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import CartSerializer
from .models import Cart, CartItem
from products.models import ProductModel

class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']  # Allow PATCH explicitly

    # GET /cart/
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # POST /cart/add/
    def create(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        # Validate product_id and quantity
        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Quantity must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the product exists
        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if there is enough stock
        if product.stock < quantity:
            return Response({
                "error": "Not enough stock available",
                "available_stock": product.stock,
                "requested_quantity": quantity
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create the CartItem
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Set the quantity explicitly
        cart_item.quantity = quantity
        cart_item.save()

        # Update the product stock
        product.stock -= quantity
        product.save()

        return Response({
            "message": "Product added to cart",
            "cart_item": {"id": cart_item.id, "quantity": cart_item.quantity},
            "product_stock": product.stock
        }, status=status.HTTP_200_OK)

    # PATCH /cart/update/<id>/
    def partial_update(self, request, pk=None):
        if pk is None:
            return Response({"error": "Cart item ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        quantity = request.data.get("quantity")
        if not quantity or int(quantity) <= 0:
            return Response({"error": "Quantity must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                "error": "Cart item not found",
                "details": f"No CartItem with id {pk} for user {request.user.username}"
            }, status=status.HTTP_404_NOT_FOUND)

        # Validate stock availability before updating the CartItem
        product = ProductModel.objects.get(id=cart_item.product.id)
        new_quantity = int(quantity)
        stock_change = new_quantity - cart_item.quantity

        if stock_change > 0 and product.stock < stock_change:
            return Response({
                "error": "Not enough stock available",
                "available_stock": product.stock,
                "requested_quantity": new_quantity
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update the CartItem quantity and ProductModel stock
        cart_item.quantity = new_quantity
        cart_item.save()

        product.stock -= stock_change
        product.save()

        return Response({
            "message": "Quantity updated",
            "cart_item": {"id": cart_item.id, "quantity": cart_item.quantity},
            "product_stock": product.stock
        })

    # DELETE /cart/remove/<id>/
    def destroy(self, request, pk=None):
        if pk is None:
            return Response({"error": "Cart item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                "error": "Cart item not found",
                "details": f"No CartItem with id {pk} for user {request.user.username}"
            }, status=status.HTTP_404_NOT_FOUND)

        # Restore the product stock
        product = cart_item.product
        product.stock += cart_item.quantity
        product.save()

        # Delete the CartItem
        cart_item.delete()

        return Response({
            "message": "Item removed from cart",
            "product_stock": product.stock
        })
