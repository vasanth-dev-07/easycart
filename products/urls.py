from django.urls import path
from .views import ProductCRUDApi

urlpatterns = [
    path('product/', ProductCRUDApi.as_view(), name='product-list'),
    path('product/<str:name>/',ProductCRUDApi.as_view()),
    ]