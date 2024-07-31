from Client_provider.models import Location,Service,Provider_employee,Therapist
from rest_framework import serializers



class ServiceSerializerdetail(serializers.ModelSerializer):
    id = serializers.IntegerField(source='service_id', read_only=True)
    label = serializers.CharField(source='service_name', read_only=True)
    type = serializers.CharField(source='service_type', read_only=True)
    serviceDescription = serializers.CharField(source='service_description', read_only=True)
    serviceActive = serializers.BooleanField(default=True)

    class Meta:
        model = Service
        fields = ['id', 'label', 'type', 'serviceDescription', 'serviceActive']


class LocationSerializerdetail(serializers.ModelSerializer):
    id = serializers.IntegerField(source='location_id', read_only=True)
    label = serializers.CharField(source='location_name', read_only=True)
    locationDescription = serializers.CharField(source='location_description', read_only=True)
    class Meta:
        model = Location
        fields = ['id','label','locationDescription']


class therapistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    label = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Therapist
        fields = ["id", "label", "specialization","experience"]

    def get_label(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"

class ProviderEmployee(serializers.ModelSerializer):
    employeeId= serializers.IntegerField(source='id', read_only=True)
    label = serializers.CharField(source='usersName', read_only=True)
    type = serializers.CharField(source='userType', read_only=True)
   
    class Meta:
        model = Provider_employee
        fields = ["employeeId", "label","type"]