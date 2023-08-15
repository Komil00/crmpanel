from rest_framework import serializers
from main.models import User 
from .models import Comment
from .utils import *




class CreateUserProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=18)
    surname = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=14)

    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists")
        return value

    def validate_phone(self,phone):
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone number is registered")
        return phone        

    def save(self, validated_data):
        data = dict(validated_data)
        phone = data.pop('phone')

        try:
            user = User.objects.get(username=phone)
            return False 
        except:
            u = False 
        try:
            p = User.objects.get(phone=phone)
            p.user = user
            p.verification_code=CreateVerificationCode()
            p.save()
            # p.send_verification_code()
        except:    
            user_profile = User.objects.create_user(
                                username=phone,
                                password=phone,
                                phone=phone,
                                first_name=validated_data['name'], 
                                last_name=validated_data['surname'],
                                is_active=False,
                                verification_code=CreateVerificationCode()
            )
            # user_profile.send_verification_code()
            user_profile.user_type = "customer"
            user_profile.save()
        return user_profile.verification_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","last_login","first_name","last_name","date_joined","phone","user_type")

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"