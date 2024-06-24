
from .models import User_mobile
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models  import User_mobile
from datetime import datetime


class User_mobile_serialize(serializers.ModelSerializer):
    dateofBirth = serializers.DateField(input_formats=['%d/%m/%Y'], format='%d/%m/%Y', required=False)
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber', 'password', 'communicationPreference', 'refferalCode', 'signingAs']
    
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.dateofBirth:
    #         representation['dateofBirth'] = instance.dateofBirth.strftime('%d/%m/%Y')
    #     return representation
    
    # def to_internal_value(self, data):
    #     if 'dateofBirth' in data:
    #         data['dateofBirth'] = datetime.strptime(data['dateofBirth'], '%Y/%d/%m').date()
    #     return super().to_internal_value(data)
        

class LoginAPIView(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    

class UserMobileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber', 'communicationPreference', 'signingAs']
        
    




