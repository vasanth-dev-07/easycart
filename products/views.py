from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import  ProductSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView,status
from .models import ProductModel
from rest_framework.permissions import AllowAny,IsAdminUser
from .permission import IsAdminOrReadOnly   

class ProductList(ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class ProductCRUDApi(APIView):
    def get(self,request,*args,**kwargs):
        product_name = kwargs.get('name')
        if product_name:
            product = ProductModel.objects.get(name=product_name)
            serailizer = ProductSerializer(product,many=False)
            return Response(serailizer.data,status=status.HTTP_200_OK)
        else:
            product = ProductModel.objects.all()
            serailizer = ProductSerializer(product,many=True)
            return Response(serailizer.data,status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):
        serailzer = ProductSerializer(data=request.data)
        if serailzer.is_valid():
            serailzer.save()    
            return Response(serailzer.data,status=status.HTTP_201_CREATED)
        return Response(serailzer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put (self,request,*args,**kwargs):
        name = kwargs.get("name")

        try:
            product = ProductModel.objects.get(name=name)
        except ProductModel.DoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        if product:
            serializer = ProductSerializer(product,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete (self,request,*args,**kwargs):
        product_name = kwargs.get('name')
        try:
            product = ProductModel.objects.get(name=product_name)
        except ProductModel.DoesNotExist:
            return Response({'error':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        if product:
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        

class FilterApi(APIView):
    def get(self,request,*args,**kwargs):
        # Extract query parameters
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')
        products = ProductModel.objects.all()
        if category:
            products = products.filter(category__name = category)
        if subcategory:
            products = products.filter(subcategory__name = subcategory)
        serializer = ProductSerializer(products,many = True)
        return Response(serializer.data)








