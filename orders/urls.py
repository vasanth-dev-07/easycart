from django.urls import path,include
from . import views
from .views import OrderCreateApiView,AddCartApiView,ViewCartAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     path('addcart/', AddCartApiView.as_view(), name='addcart'),
     path('orders/', OrderCreateApiView.as_view(), name='orders'),
     path('viewcart/', ViewCartAPIView.as_view(), name='viewcart'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]