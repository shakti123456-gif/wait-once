
from rest_framework import serializers
from .models import Provider,Therapist,Location,Service,Therapist_working_time ,\
    Therapist_unavailability ,Appointment1,Appointment,Provider_employee
from mobile_api_user.Serializer import UserMobileSerializerfetchdata

class ProviderSerializer(serializers.ModelSerializer):
    contactInfo = serializers.EmailField(source='email')
    class Meta:
        model = Provider
        fields = ["providerId","providerName","contactInfo"]

class therapistSerializer(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    therapistFullName = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Therapist
        fields = ["therapistId", "therapistFullName", "specialization","experience"]

    def get_therapistFullName(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"
    

class therapistSerializerAppointment(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    therapistFullName = serializers.SerializerMethodField(read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)

    class Meta:
        model = Therapist
        fields = ["therapistId", "therapistFullName","specialization"]


    def get_therapistFullName(self, obj):
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

class ServiceSerializerdetailAppointment(serializers.ModelSerializer):
    serviceId = serializers.IntegerField(source='service_id', read_only=True)
    serviceName = serializers.CharField(source='service_name', read_only=True)
    serviceType = serializers.CharField(source='service_type', read_only=True)

    class Meta:
        model = Service
        fields = ['serviceId','serviceName','serviceType']

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
              'abn','ageGroup','web','chain','dva',
              'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']
        read_only_fields = fields


class TherapistWorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Therapist_working_time
        fields = '__all__'


class Therapist_unavailability(serializers.ModelSerializer):
    class Meta:
        model= Therapist_unavailability
        fields = '__all__'



class AppointmentSerializer1(serializers.ModelSerializer):
    clientId = serializers.StringRelatedField()
    childId = serializers.StringRelatedField()
    provider = serializers.StringRelatedField()  
    therapist = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    class Meta:
        model = Appointment
        # fields = ['clientData','childId','providerData','therapistData','serviceData','LocationData','appointmentDate','TherapyTime_start','TherapyTime_end','Location_details','status','isconfimed'



class AppointmentSerializer(serializers.Serializer):
    appointmentId = serializers.IntegerField()

class RescheduleAppointmentSerializer(serializers.Serializer):
    appointmentId = serializers.IntegerField()
    rescheduleAppointmentDate = serializers.DateField(input_formats=['%d-%m-%Y'])
    rescheduleTime = serializers.TimeField(input_formats=['%H:%M:%S'])


class AppointmentSerializerfetch(serializers.ModelSerializer):
    appointmentId= serializers.IntegerField(source='id', read_only=True)
    clientData = UserMobileSerializerfetchdata(read_only=True)
    providerData = ProviderSerializer(read_only=True)
    therapistData = therapistSerializerAppointment(read_only=True)
    serviceData = ServiceSerializerdetail(read_only=True)
    locationData = LocationSerializerdetail(read_only=True)
    therapyStartTime = serializers.TimeField(source='TherapyTime_start', read_only=True)
    therapyEndTime = serializers.TimeField(source='TherapyTime_end', read_only=True)
    isConfimed = serializers.BooleanField(source='isconfimed', read_only=True)

    class Meta:
        model = Appointment1
        fields = ['appointmentId','clientData','providerData','therapistData','serviceData','locationData','appointmentDate','therapyStartTime','therapyEndTime','status','isConfimed']


class TherapistAvailSerializer(serializers.Serializer):
    availablityDate = serializers.DateField(input_formats=['%d-%m-%Y'])


class clientBooking(serializers.Serializer):
    availablityDate = serializers.DateField(input_formats=['%d-%m-%Y'])


class TherapistSerializerweb(serializers.ModelSerializer):
    therapistId = serializers.IntegerField(source='therapist_id', read_only=True)
    specialization = serializers.CharField(source='therapist_type', read_only=True)
    therapistFullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Therapist
        fields = ["therapistId", "therapistFullname", "specialization","experience"]

    def get_therapistFullname(self, obj):
        therapist_auth = obj.therapist_auth  
        if therapist_auth:
            return f"{therapist_auth.firstName} {therapist_auth.lastName}"
        return "Not added"

class ProviderEmployee(serializers.ModelSerializer):
    employeeId= serializers.IntegerField(source='id', read_only=True)
   
    class Meta:
        model = Provider_employee
        fields = ["employeeId", "usersName","password","userType"]


class ProviderSerializerdetailWeb(serializers.ModelSerializer):
    label = serializers.CharField(source='providerName')
    class Meta:
        model = Provider
        fields = ['id','label','providerNum','providerType','email','ndisNumber',
              'abn','ageGroup','web','chain','dva',
              'alternativeMobileNumber','permanentAddress1','permanentAddress2','city',
              'state','pin','additionalInfo1','additionalInfo2','additionalInfo3','additionalInfo4']
        read_only_fields = fields