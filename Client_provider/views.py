from mobile_api_user.authentication import JWTAuthentication
from rest_framework import generics
from .models import Provider,Therapist,Service,therapist_service,Therapist_working_time,Therapist_unavailability
from .Serializers import ProviderSerializer,therapistSerializer,ProviderSerializerdetail,LocationSerializerdetail,ServiceSerializerdetail
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer

    def get_queryset(self):
        queryset=Provider.objects.all()
        provider_name = self.request.data.get('providerName', None)
        pin_code = self.request.data.get('pincode', None)
        if provider_name:
            queryset = queryset.filter(providerName__contains=provider_name)
        if pin_code:
            queryset = queryset.filter(PIN=pin_code)

        return queryset

    @action(detail=True,methods=['post'])
    def fetch_providers(self,request,pk=None):
        provider=self.get_queryset()
        if not provider:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': 'Data is not available',
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)            
        serializer=ProviderSerializer(provider,many=True)
        return Response(serializer.data)
    
  
    @action(detail=True,methods=['get'])
    def list(self,request):
        provider_data=Provider.objects.all()
        serializer=ProviderSerializer(provider_data,many=True)
        return Response(serializer.data)

    @action(detail=True,methods=['get'])
    def details_provider(self,request,pk=None):
        try:
            provider_data=Provider.objects.filter(providerId=pk).first()
            if not provider_data:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Provider user Id is not exit',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            therapist_details,service_details=provider_data.therapist_and_service_details
            locations_data=provider_data.Provider_locations_add
            location_serializer = LocationSerializerdetail(locations_data, many=True)
            therapist_serializer = therapistSerializer(therapist_details, many=True)
            service_serializer = ServiceSerializerdetail(service_details, many=True)
            provider_serializer = ProviderSerializerdetail(provider_data)
            serialized_data = provider_serializer.data
            serialized_data['locations'] = location_serializer.data
            serialized_data['therapist'] = therapist_serializer.data
            serialized_data['services'] = service_serializer.data
            return Response(serialized_data)
        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': str(e),
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)     
    

    @action(detail=True,methods=['get'])
    def details_provider_therapist(self,request):
        data_pd_id=request.headers.get("providerId","None")
        therapist_pd_id=request.headers.get("therapistId","None")
        try:
            print(therapist_pd_id,data_pd_id)
            provider_data=Provider.objects.filter(providerId=data_pd_id).first()
            data = provider_data.get_therapist_services(therapist_pd_id)
            service_serializer = ServiceSerializerdetail(data, many=True)
            return Response(service_serializer.data)     
        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': str(e),
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)     
    
    @action(detail=True,methods=['get'])
    def details_provider_service(self,request,pk=None):
        try:
            provider_data=Provider.objects.filter(providerId=pk).first()
            if not provider_data:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Provider user Id is not exit',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            service_details=provider_data.service_details
            service_serializer = ServiceSerializerdetail(service_details, many=True)
            return Response(service_serializer.data)
        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': str(e),
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)    



class TherapistViewSet(viewsets.ModelViewSet):
    serializer_class = therapistSerializer

    def get_queryset(self, therapist_id=None):
        try:
            queryset = Therapist.objects.get(therapist_id=therapist_id)
            therapist_working_time = Therapist_working_time.objects.filter(therapist_id=queryset)
            therapist_unava=Therapist_unavailability.objects.filter(therapist_id=queryset)
            therapist_working_time

            data={
                "Therapist_data":queryset,
                "therapist_working_time":therapist_working_time,
                "therapist_unava":therapist_unava
                }

            return data
        except Therapist.DoesNotExist:
            raise Exception("User is not Exist")

    @action(detail=True,methods=['get'])
    def fetch_therapist(self,request,pk=None):
        therapistId=request.headers.get("therapistId",None)
        data=self.get_queryset(therapistId)
        print(data)
        if not data:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': 'Data is not available',
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        return HttpResponse("Success")

    
   
    
    


