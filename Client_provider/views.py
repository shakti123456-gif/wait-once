from mobile_api_user.authentication import JWTAuthentication
from rest_framework import generics
from .models import Provider,Therapist,Service,therapist_service,Therapist_working_time,Therapist_unavailability,therapistAvailability,Appointment
from .Serializers import ProviderSerializer,therapistSerializer,ProviderSerializerdetail,LocationSerializerdetail,ServiceSerializerdetail,AppointmentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from mobile_api_user.models import Client_details_view,Client_sub_view
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer

    def get_queryset(self):
        
        provider_name = self.request.data.get('providerName', None)
        pin_code = self.request.data.get('pincode', None)
        if provider_name is None and pin_code is None :
            return []

        queryset=Provider.objects.all()
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
            data_therapist=therapist_service.objects.filter(Therapist_Name=queryset)
            details_service=[e.service_Name.service_id for e in data_therapist]
            service_data=Service.objects.filter(service_id__in=details_service)
            providers_data = Provider.objects.filter(therapistServicemap__in=data_therapist)
        
            data={
                "Therapist_data":queryset,
                "service_data":service_data,
                "providers":providers_data
                }

            return data
        except Therapist.DoesNotExist:
            raise Exception("User is not Exist")

    @action(detail=True,methods=['get'])
    def fetch_therapist(self, request, pk=None):
        therapist_id = request.headers.get("therapistId", None)
        if not therapist_id:
            response = {
                'status': 'error',
                'statusCode': 400,
                'message': 'Therapist ID is required',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        data = self.get_queryset(therapist_id)
        if not data:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': 'Data is not available',
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        service_serializer = ServiceSerializerdetail(data.get("service_data", None), many=True)
        therapist_data_serializer = therapistSerializer(data.get("Therapist_data", None))
        provider_data_serializer = ProviderSerializer(data.get("providers", None), many=True)

        response_data = {
            'status': 'success',
            'statusCode': 200,
            'Therapist_data': therapist_data_serializer.data,
            'service_data': service_serializer.data,
            'providers': provider_data_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

class Client_booking_Details(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]


    @action(detail=True,methods=['post'])
    def create_booking(self,request,pk=None):
        data=request.data
        therapist_avail=data.get("therapist",None)
        date_appointment=data.get("appointmentDate",None)
        therapy_time_start = data.get("TherapyTime_start",None)
        providerDetail=data.get("provider")
        service_id=data.get("service")
        session_time=data.get("session-time","")
        try:
            therapy_time_start = datetime.strptime(therapy_time_start, "%H:%M:%S")
        except ValueError:
            return JsonResponse({"error": "Invalid time format for TherapyTime_start"}, status=400)
        try:
        # Parse session duration
            session_hours, session_minutes = map(int, session_time.split(":"))
            session_duration = timedelta(hours=session_hours, minutes=session_minutes)
        except ValueError:
            return JsonResponse({"error": "Invalid session duration format"}, status=400)
        
        therapy_time_end = therapy_time_start + session_duration
        therapy_time_end_str = therapy_time_end.strftime("%H:%M:%S")

        if therapist_avail:
            therapist_avail_date=therapistAvailability.objects.filter(therapist_id__therapist_id=therapist_avail,
                                                                      date=date_appointment).first()
            if therapist_avail_date:
                appointments = Appointment.objects.filter(
                        appointmentDate=date_appointment, 
                        therapistId=therapist_avail_date.therapist_id.therapist_id,isconfimed=True)
                for apointment in appointments:
                    appointment_start = timedelta(hours=apointment.TherapyTime_start.hour, minutes=apointment.TherapyTime_start.minute)
                    appointment_end = timedelta(hours=apointment.TherapyTime_end.hour, minutes=apointment.TherapyTime_end.minute)

                # Calculate new appointment start and end times as timedelta durations
                    new_appointment_start = timedelta(hours=therapy_time_start.hour, minutes=therapy_time_start.minute)
                    new_appointment_end = new_appointment_start + session_duration

                # Check if new appointment overlaps with any existing appointment
                    if (new_appointment_start < appointment_end and new_appointment_end > appointment_start):
                        return JsonResponse({"error": "Appointment already booked at this time"}, status=409)
                  
                    # therapy_time_start   not between appointment.TherapyTime_start   and appointmente.TherapyTime_end
                    # appointment.TherapyTime_start   not between appointment.TherapyTime_start   and appointmente.TherapyTime_end
            else:
                return HttpResponse("Therapist data is not updated from database")
            
            print(request.user.userId)                        
        
            provider=Provider.objects.filter(providerId=providerDetail).first()
            service=Service.objects.filter(service_id=service_id).first()
            new_appointment = Appointment(
                clientId=request.user.userId,
                providerId=provider.providerId,
                therapistId=therapist_avail_date.therapist_id.therapist_id,
                serviceId=service.service_id,
                appointmentDate=date_appointment,
                TherapyTime_start=therapy_time_start,
                TherapyTime_end=therapy_time_end,
                Location_details=data.get("Location_details"),
                status="confirmed",
                isconfimed=True
            )
            new_appointment.save()
        
        return HttpResponse("Appointmentbooking is done ")
   
    
    


