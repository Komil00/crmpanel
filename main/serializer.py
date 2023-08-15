from rest_framework import serializers
from .models import Bron , Category ,Service, ServicePhotos


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BronSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bron
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class ServicePhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePhotos
        fields = "__all__"