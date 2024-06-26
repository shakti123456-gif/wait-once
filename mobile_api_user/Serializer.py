
from .models import User_mobile
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models  import User_mobile,Client_sub_view,Client_details_view
from datetime import datetime


class UserMobileSerializer(serializers.ModelSerializer):
    dateofBirth = serializers.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = User_mobile
        fields = [
            'firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
            'ndisNumber', 'password', 'communicationPreference', 'refferalCode', 'signingAs'
        ]

class ClientSubSerializer(serializers.ModelSerializer):
    dateofBirth = serializers.DateField(input_formats=['%d/%m/%Y'], required=False, source='dateofbirth')

    class Meta:
        model = Client_sub_view
        fields = ['first_name', 'last_name', 'dateofBirth', 'Ndisnumber']

class ClientDetailSerializer(serializers.ModelSerializer):
    ClientAuth = UserMobileSerializer(read_only=True)
    addCaretakerDetail = ClientSubSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Client_details_view
        fields = ['ClientAuth', 'addCaretakerDetail']
 

class LoginAPIView(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    

class UserMobileSerializerfetch(serializers.ModelSerializer):    
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber', 'communicationPreference', 'signingAs']
        



        
    




