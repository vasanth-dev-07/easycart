from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserLoginModelViewSet , SigninApiView,LogoutApiView,ContactUsApiView,SendOtpApiView,ValidateOtp,ResetPassword
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



router = DefaultRouter()
router.register('register', UserLoginModelViewSet) 

urlpatterns = [
    path('', include(router.urls)),
      
    path('logout/', LogoutApiView.as_view(), name='logout'),  
    path('sendotp/', SendOtpApiView.as_view(), name='otp'),  
    path('validateotp/', ValidateOtp.as_view(), name='validateotp'),  
    path('resetpassword/', ResetPassword.as_view(), name='resetpassword'),  
    path('signin/', SigninApiView.as_view(), name='signin'),    
    path('login/', TokenObtainPairView.as_view(), name='login'),    
    path('contact/', ContactUsApiView.as_view(), name='contact'),    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]