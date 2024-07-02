
from rest_framework import serializers
from .models import Provider,Therapist,Location,Service,Therapist_working_time

class ProviderSerializer(serializers.ModelSerializer):
    # providerId=serializers.EmailField(source='provider_id')
    contactInfo = serializers.EmailField(source='email')
    # providerName=serializers.EmailField(source='provider_name')
    class Meta:
        model = Provider
        fields = ["providerId","providerName","contactInfo"]

class therapistSerializer(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    therapistFullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Provider
        fields = ["therapistId", "therapistFullname", "specialization"]

    def get_therapistFullname(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"

class ServiceSerializerdetail(serializers.ModelSerializer):
    serviceId = serializers.IntegerField(source='service_id', read_only=True)
    serviceName = serializers.CharField(source='service_name', read_only=True)
    serviceType = serializers.CharField(source='service_type', read_only=True)
    serviceDescription = serializers.CharField(source='service_description', read_only=True)
    class Meta:
        model = Service
        fields = ['serviceId','serviceName','serviceType','serviceDescription']

class LocationSerializerdetail(serializers.ModelSerializer):
    locationId = serializers.IntegerField(source='location_id', read_only=True)
    locationName = serializers.CharField(source='location_name', read_only=True)
    locationDescription = serializers.CharField(source='location_description', read_only=True)
    class Meta:
        model = Location
        fields = ['locationId','locationName','locationDescription']


class ProviderSerializerdetail(serializers.ModelSerializer):
    # services = ServiceSerializerdetail(many=True)
    # locations = LocationSerializerdetail(many=True)
    # therapist = therapistSerializer(many=True)

    class Meta:
        model = Provider
        fields = ['providerName','providerNum','providerType','email','ndisNumber',
              'abn','ageGroup','web','chain','phoneNo', 
              'AlternativeMobileNumber','PermanentAddress1','PermanentAddress2','City',
              'State','PIN','AdditionalInfo1','AdditionalInfo2','AdditionalInfo3','AdditionalInfo4']
        read_only_fields = fields


class TherapistWorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist_working_time
        fields = '__all__'


