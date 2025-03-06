from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView,status

class UserLoginModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user':serializer.data,
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST,
            )




