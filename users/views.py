from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer ,ContactUsSerailizer 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView,status
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate
from .models import PasswordResetOtp
import random


class UserLoginModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            refresh = RefreshToken.for_user(user)
            email = EmailMessage(
                        "you are registered succesfully !",
                        "Welcome to our Ecommerce Platform !!!",
                        to = [serializer.validated_data['email']]
                    )
            email.send()
            return Response({
                'user':serializer.data,
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST,
            )

class SigninApiView(APIView):
    def post(self, request):
        user_name = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = user_name,password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message':'login succesfully !!!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutApiView(APIView):
    def post(self,request):
        return Response ({'message':"Logout Successfully !!!"})
    
class ContactUsApiView(APIView):
    def post(self,request):
        name = request.data.get('name')
        email = request.data.get('email')
        description = request.data.get('description')
        phonenumber = request.data.get('phonenumber')
        serializer = ContactUsSerailizer (data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message: we will reach back soon'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendOtpApiView(APIView):
    def post(self,request):
        email = request.data.get('email')
        if not email :
            return Response({'Error':'Email is Required'},status=status.HTTP_404_NOT_FOUND)
        try : 
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response({'Error':'User Not Found'},status=status.HTTP_404_NOT_FOUND)
        otp = str(random.randint(100000,999999))
        PasswordResetOtp.objects.create(user=user,otp=otp)
        email = EmailMessage(
                        "otp for Password change!",
                        f'you otp to change the passowrd is {otp}',
                        to = [email]
                    )
        email.send()
        return Response({'message':'Otp sent to you email id to change change password'})

class ValidateOtp(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')

        try:
            otp_obj = PasswordResetOtp.objects.filter(user__email=email).last()

            if not otp_obj:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if str(otp_obj.otp) == str(otp):
                return Response({'message': 'OTP accepted'}, status=status.HTTP_202_ACCEPTED)

            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ResetPassword(APIView):
    def post(self,request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        user = PasswordResetOtp.objects.filter(user__email = email,otp = otp).last()
        try:
            user = User.objects.get(email=email)
            otp_record = PasswordResetOtp.objects.filter(user = user,otp = otp).last()
            if otp_record:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    otp_record.delete()
                    return Response({'message':'password changed sucessfully!'})
                return Response({'message':'both password must same'},status=status.HTTP_202_ACCEPTED)
            return Response({'message':'Invalid Otp !!!'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message':'User not Found'},status=status.HTTP_400_BAD_REQUEST)




