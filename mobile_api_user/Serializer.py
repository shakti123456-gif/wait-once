
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
    dateOfBirth = serializers.DateField(input_formats=['%d/%m/%Y'], required=False, source='dateofbirth')

    class Meta:
        model = Client_sub_view
        fields = ['firstName', 'lastName', 'dateOfBirth', 'insurance']

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
        
class ClientDetailsViewSerializers(serializers.ModelSerializer):
    clientId = serializers.IntegerField(read_only=True, source='Client_ID')
    clientDetails = UserMobileSerializerfetch(read_only=True, source='Client_auth')
    childrenDetails = ClientSubSerializer(many=True, read_only=True, source='addChildren')

    class Meta:
        model = Client_details_view
        fields = ['clientId','clientDetails','childrenDetails', 'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'childrenDetails' in representation and not representation['childrenDetails']:
            del representation['childrenDetails']
        return representation

        
class UserMobileSerializerfetchdata(serializers.ModelSerializer):    
    class Meta:
        model = User_mobile
        fields = ['firstName', 'lastName', 'dateofBirth', 'mobileNumber', 'email',
                  'ndisNumber']
        

# class UserMobileSerializerfetch(serializers.ModelSerializer):    
#     class Meta:
#         model = Client_sub_view
#         fields = ['first_name', 'last_name', 'dateofBirth', 'Ndisnumber']
        


        
    




