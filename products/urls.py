from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import ProductCRUDApi, FilterApi, ProductList
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('products', ProductList, basename='product-list')  # Register the ViewSet with the router

urlpatterns = [
    path('', include(router.urls)),  # Include router-generated URLs
    path('product/', ProductCRUDApi.as_view(), name='product'),
    path('product/<str:name>/', ProductCRUDApi.as_view()),
    path('filter/', FilterApi.as_view(), name='filter'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token endpoint
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)