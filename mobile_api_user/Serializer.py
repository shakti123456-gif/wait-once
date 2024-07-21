
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
            'ndisNumber', 'password', 'communicationPreference', 'refferalCode', 'signingAs','createdAt','lastUpdate'
        ]

class ClientSubSerializer(serializers.ModelSerializer):
    dateofBirth = serializers.DateField(input_formats=['%d/%m/%Y'], required=False, source='dateofbirth')

    class Meta:
        model = Client_sub_view
        fields = ['firstName', 'lastName', 'dateofBirth', 'insurance']

class ClientDetailSerializer(serializers.ModelSerializer):
    ClientAuth = UserMobileSerializer(read_only=True)
    addChildren = ClientSubSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Client_details_view
        fields = ['ClientAuth', 'addChildren']

class ClientDetailsViewSerializer(serializers.ModelSerializer):
    addChildren = serializers.SerializerMethodField()
    Client_auth = serializers.StringRelatedField()  # or serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Client_details_view
        fields = ['Client_ID', 'Client_auth', 'Type', 'addChildren']

    def get_addChildren(self, obj):
        children = obj.addChildren.all()
        if children.exists():
            return ClientSubSerializer(children, many=True).data
        return None  # or []

 

class LoginAPIView(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    

class UserMobileSerializerfetch(serializers.ModelSerializer):    
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber', 'communicationPreference', 'signingAs']
        
class ClientDetailsViewSerializers_percentage(serializers.ModelSerializer):
    user_mobile = UserMobileSerializerfetch(read_only=True)

    class Meta:
        model = Client_details_view
        fields ='__all__'
        
class UserMobileSerializerfetchdata(serializers.ModelSerializer):    
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber']
        

# class UserMobileSerializerfetch(serializers.ModelSerializer):    
#     class Meta:
#         model = Client_sub_view
#         fields = ['first_name', 'last_name', 'dateofBirth', 'Ndisnumber']
        


        
    




