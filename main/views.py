# from django.shortcuts import render
from distutils.sysconfig import customize_compiler
from customer.errors import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from main.models import Service, User,Category
from customer.utils import MyResponse
from .serializer import CategorySerializer,ServiceSerializer,ServicePhotosSerializer
from customer.serializer import CommentSerializer
from django.shortcuts import get_object_or_404
# Create your views here.

class CategoryApiView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = Category.objects.all().order_by('-id') 
        serilizer = CategorySerializer(queryset, many=True)
        return MyResponse(serializer_objects=serilizer.data,error_status=SUCCESS)

    def retrieve(self,request,pk):
        category = get_object_or_404(Category,pk=pk)
        services = Service.objects.filter(category=category)
        serilizer = ServiceSerializer(services, many=True)     
        return MyResponse(serializer_objects=serilizer.data,error_status=SUCCESS)

class ServiceApiView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = Category.objects.all().order_by('-id') 
        serilizer = CategorySerializer(queryset, many=True)
        return MyResponse(serializer_objects=serilizer.data,error_status=SUCCESS)

    def retrieve(self,request,pk):
        service = get_object_or_404(Service,pk=pk)
        serilizer = ServiceSerializer(service, many=False)  
        photos =  ServicePhotosSerializer(service.service_photos.all(), many=True) 
        comments =  CommentSerializer(service.comments.all(), many=True) 
        return MyResponse(serializer_objects=serilizer.data,error_status=SUCCESS,service_photos=photos.data,
            comments=comments.data)



category_api_view =   CategoryApiView.as_view({'get':"list"}) 
category_detail_view =   CategoryApiView.as_view({'get':"retrieve"}) 
service_detail_view =   ServiceApiView.as_view({'get':"retrieve"}) 