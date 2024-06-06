
from .models import User_mobile,Service
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class User_mobile_serialize(serializers.ModelSerializer):
    class Meta:
        model = User_mobile
        fields = ['first_name', 'last_name', 'Dateofbirth', 'mobile_number', 'email_address', 
                  'ndis_number','password']
        
class LoginAPIView(serializers.Serializer):
    phonenumber = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)


class UserMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_mobile
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'  #