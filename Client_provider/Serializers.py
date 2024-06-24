
from rest_framework import serializers
from .models import Provider,Therapist,Location

class ProviderSerializer(serializers.ModelSerializer):
    contact_info = serializers.EmailField(source='email')
    name=serializers.EmailField(source='provider_name')
    class Meta:
        model = Provider
        fields = ["provider_id","name","contact_info"]

class therapistSerializer(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    therapistFullname = serializers.SerializerMethodField(read_only=True)  # Combined field

    class Meta:
        model = Provider
        fields = ["therapistId", "therapistFullname", "specialization"]

    def get_therapistFullname(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"
    

class therapistSerializer(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    therapistFullname = serializers.SerializerMethodField(read_only=True)  # Combined field

    class Meta:
        model = Location
        fields = ["therapistId", "therapistFullname", "specialization"]

    def get_therapistFullname(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"
