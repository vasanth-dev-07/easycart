from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'patch': 'partial_update',  # Map PATCH to partial_update
    'delete': 'destroy',
})

urlpatterns = [
    path('cart/', cart_list, name='cart'),
    path('cart/<int:pk>/', cart_list, name='cart-detail'),  # Include pk for item-specific actions
]
