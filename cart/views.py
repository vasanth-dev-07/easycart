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
    # MAX_LIMIT = 10
    # GET /cart/
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # POST /cart/add/
    def create(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        MAX_LIMIT = 10

        if not product_id:
            return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return Response({"error": "Quantity must be a positive integer"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = ProductModel.objects.get(id=product_id)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if product.stock < quantity:
            return Response({
                "error": "Not enough stock available",
                "available_stock": product.stock,
                "requested_quantity": quantity
            }, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            original_qty = cart_item.quantity
            new_total = original_qty + quantity

            if new_total > MAX_LIMIT:
                allowed = MAX_LIMIT - original_qty

                if allowed <= 0:
                    return Response({"message": f"Limit reached. Added only {allowed}. Maximum {MAX_LIMIT} units allowed per product."},
                                    status=status.HTTP_200_OK)

                cart_item.quantity = MAX_LIMIT
                cart_item.save()

                product.stock -= allowed
                product.save()

                return Response(
                    {"message": f"Limit reached. Added only {allowed}. Maximum {MAX_LIMIT} allowed."},
                    status=status.HTTP_200_OK
                )

            cart_item.quantity = new_total
            cart_item.save()
            product.stock -= quantity
            product.save()

        else:
            if quantity > MAX_LIMIT:
                allowed = MAX_LIMIT
                cart_item.quantity = MAX_LIMIT
                cart_item.save()
                product.stock -= MAX_LIMIT
                product.save()
                return Response(
                    {"message": f"Limit reached. Added only {allowed}. Maximum {MAX_LIMIT} units allowed per product."},
                    status=status.HTTP_200_OK
                )

            cart_item.quantity = quantity
            cart_item.save()
            product.stock -= quantity
            product.save()

        return Response(
            {
                "message": "Product added to cart",
                "cart_item": {"id": cart_item.id, "quantity": cart_item.quantity},
                "product_stock": product.stock
            }, status=status.HTTP_200_OK
        )


    # PATCH /cart/update/<id>/
    def partial_update(self, request, pk=None):
        quantity = request.data.get("quantity")
        MAX_LIMIT = 10

        if pk is None:
            return Response({"error": "Cart item ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert quantity to int
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({"error": "Quantity must be a valid number"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        product = ProductModel.objects.get(id=cart_item.product.id)

        # If quantity is zero -> remove item & restore stock
        if quantity == 0:
            product.stock += cart_item.quantity
            product.save()
            cart_item.delete()
            return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

        # Validate limit
        # If requested quantity exceeds limit or stock, adjust to what is possible
        if quantity > MAX_LIMIT:
            allowed_addition = MAX_LIMIT - cart_item.quantity
            if allowed_addition > 0:
                product.stock -= allowed_addition
                product.save()
                cart_item.quantity = MAX_LIMIT
                cart_item.save()

                return Response(
                    {"message": f"Limit reached. Added only {allowed_addition}. Max {MAX_LIMIT} allowed."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": f"Product already at max limit {MAX_LIMIT}"},
                    status=status.HTTP_400_BAD_REQUEST
                )


        # Check stock availability when increasing
        if quantity > cart_item.quantity:
            diff = quantity - cart_item.quantity
            if product.stock < diff:
                return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
            product.stock -= diff  # decrease stock

        else:
            diff = cart_item.quantity - quantity
            product.stock += diff  # returning stock

        # Save updates
        cart_item.quantity = quantity
        cart_item.save()
        product.save()

        return Response({
            "message": "Quantity updated",
            "cart_item": {"id": cart_item.id, "quantity": cart_item.quantity},
            "product_stock": product.stock
        }, status=status.HTTP_200_OK)


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
