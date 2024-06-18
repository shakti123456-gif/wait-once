
from .models import User_mobile
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models  import User_mobile


class User_mobile_serialize(serializers.ModelSerializer):
    class Meta:
        model = User_mobile
        fields = ['FirstName', 'LastName', 'DateofBirth', 'MobileNumber', 'EmailAddress',
                  'NdisNumber', 'password', 'Language', 'RefferalCode', 'Signing_as']
        
class LoginAPIView(serializers.Serializer):
    Username = serializers.CharField(max_length=200)
    Password = serializers.CharField(max_length=200)
    

class UserMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_mobile
        fields = '__all__'



class CustomTokenObtainPairSerializer(serializers.Serializer):
    mobile_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        mobile_number = data.get("mobile_number")
        password = data.get("password")
        user = User_mobile.objects.filter(mobile_number=mobile_number).first()
        if user:
            refresh = RefreshToken.for_user(user)
            data['token'] = str(refresh.access_token)
            data['refresh'] = str(refresh)
        else:
            raise serializers.ValidationError("Invalid credentials")
        return data
