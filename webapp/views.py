from django.shortcuts import render
from Client_provider.models import Provider
from Client_provider.Serializers import ProviderSerializerdetail
from .Serializers import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action



class ProviderViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['get'])
    def details_provider(self, request, pk=None):
        try:
            provider_key = request.headers.get('providerId')
            provider_data = Provider.objects.filter(providerId=1).first()
            if not provider_data:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Provider user Id does not exist',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            therapist_details,service_details=provider_data.therapist_and_service_details
            locations_data=provider_data.Provider_locations_add
            dataEmployee=provider_data.ProviderEmployee
            location_serializer = LocationSerializerdetail(locations_data, many=True)
            therapist_serializer = therapistSerializer(therapist_details, many=True)
            service_serializer = ServiceSerializerdetail(service_details, many=True)
            provider_serializer = ProviderSerializerdetailWeb(provider_data)
            dataEmployeeSerializer=ProviderEmployee(dataEmployee,many=True)
            serialized_data = provider_serializer.data
            serialized_data['children'] = [
                {
                    'id': '1',
                    'label': 'services',
                    'children': service_serializer.data
                },
                {
                    'id': '2',
                    'label': 'employees',
                    'children': dataEmployeeSerializer.data
                },
                {
                    'id': '3',
                    'label': 'therapists',
                    'children': therapist_serializer.data
                },
                {
                    'id': '4',
                    'label': 'locations',
                    'children': location_serializer.data
                }
            ]
            response = {
                'status': 'success',
                'statusCode': 200,
                'message': 'Request successful',
                'data': serialized_data
                }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': str(e),
                }
            return Response(response, status=status.HTTP_404_NOT_FOUND)     
