from mobile_api_user.authentication import JWTAuthentication
from rest_framework import generics
from .models import Provider,Therapist,Service,therapist_service,Therapist_working_time,Location,therapistAvailability,Appointment,Appointment1
from .Serializers import ProviderSerializer,therapistSerializer,ProviderSerializerdetail,LocationSerializerdetail,ServiceSerializerdetail,AppointmentSerializer,AppointmentSerializerfetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.http import HttpResponse
from mobile_api_user.models import Client_details_view,Client_sub_view
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
import json
from .Serializers import TherapistAvailSerializer ,clientBooking,TherapistSerializerweb


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
        response = {
            'status': 'success',
            'statusCode': 200,
            'message': 'Request successful',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
  
    @action(detail=True,methods=['get'])
    def list(self,request):
        provider_data=Provider.objects.all()
        serializer=ProviderSerializer(provider_data,many=True)
        response = {
            'status': 'success',
            'statusCode': 200,
            'message': 'Request successful',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
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
    @action(detail=True,methods=['get'])
    def therapist_availablity(self, request, pk=None):
        try:
            serializer = TherapistAvailSerializer(data=request.data)
            if serializer.is_valid():
                data_avail = serializer.validated_data.get("availablityDate")
                therapist_data = therapistAvailability.objects.get(date=data_avail)
                slots = therapist_data.available_slots
                data_objects=Appointment1.objects.filter(appointmentDate=data_avail).all()
                booked_slots = []
                available_slots=[]
            
                for data_iter in data_objects:
                    booked_slots.append(str(data_iter.TherapyTime_start))

                for slot in slots:
                    time1, time2 = slot.split("-")
                    is_booked = str(time1) in booked_slots
                    available_slots.append({
                            "startTime": time1,
                            "endTime": time2,
                            "isBooked": is_booked
                        })
                response_data = {
                    'status': 'success',
                    'statusCode': 200,
                    'data': {
                        "availableSlots":available_slots
                    }
                }
                return JsonResponse(response_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': "Therapist not available on that day"
                }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True,methods=['get'])
    def therapist_availablity_booked(self, request, pk=None):
        try:
            serializer = TherapistAvailSerializer(data=request.data)
            if serializer.is_valid():
                data_avail = serializer.validated_data.get("availablityDate")
                therapist_data = therapistAvailability.objects.get(date=data_avail)
                slots = therapist_data.available_slots

                response_data = {
                    'status': 'success',
                    'statusCode': 200,
                    'therapistdata': {
                        "id": therapist_data.therapist_id.therapist_id,
                        "name": therapist_data.therapist_id.therapist_auth.firstName,
                        "slots": slots
                    }
                }
                return JsonResponse(response_data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': "Therapist not available on that day"
                }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
from rest_framework.decorators import api_view
@api_view(['GET', 'POST'])
def therapist_list(request):
    if request.method == 'GET':
        therapists = Therapist.objects.all()
        serializer = therapistSerializer(therapists, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer =therapistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




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
                                                                      date=date_appointment,Provider__providerId=providerDetail).all()
            
            # error

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
            else:
                return JsonResponse({"error": "tharapist data is not updated"}, status=409)
            
        
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
        
        return HttpResponse("Appointment booking is done ")
    
    @action(detail=True,methods=['post'])
    def create_booking1(self,request,pk=None):
        data=request.data
        therapist_avail=data.get("therapist",None)
        date_appointment=data.get("appointmentDate",None)
        therapy_time_start = data.get("therapyTimeStart",None)
        providerDetail=data.get("provider")
        service_id=data.get("service")
        session_time=data.get("sessionTime","")
        LocationId=data.get("LocationId")
        try:
            date_appointment = datetime.strptime(date_appointment, '%d-%m-%Y').strftime('%Y-%m-%d')
        except:
            return JsonResponse({"error": "please enter format day/month/year"}, status=400)


        try:
            therapy_time_start = datetime.strptime(therapy_time_start, "%H:%M:%S").time()
        except ValueError:
            return JsonResponse({"error": "Invalid time format for TherapyTime_start"}, status=400)
        # try:
        #     session_hours, session_minutes = map(int, session_time.split(":"))
        #     session_duration = timedelta(hours=session_hours, minutes=session_minutes)
        # except ValueError:
        #     return JsonResponse({"error": "Invalid session duration format"}, status=400)
        
        if therapist_avail:
            therapist_avail_date=therapistAvailability.objects.filter(therapist_id__therapist_id=therapist_avail,
                                                                   date=date_appointment,Provider__providerId=providerDetail).first()
            available=False
            if therapist_avail_date:
                data_avalable_solts=therapist_avail_date.available_slots
                for time_slot in data_avalable_solts:
                    time1,time2=time_slot.split("-")
                    timeslot1 = datetime.strptime(time1, "%H:%M:%S").time()
                    timeslot2 = datetime.strptime(time2, "%H:%M:%S").time()
                    if therapy_time_start==timeslot1:
                        available=True
                        break
                status_check="confirmed" 
                if available:
                    appointments = Appointment1.objects.filter(
                            appointmentDate=date_appointment, 
                            therapistId=therapist_avail_date.therapist_id,isconfimed=True,TherapyTime_start=timeslot1)
            
                    if appointments.exists():
                        response = {
                            'status': 'error',
                            'statusCode': 404,
                            'message': 'slot is already booked',
                        }
                        return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    response = {
                            'status': 'error',
                            'statusCode': 404,
                            'message': 'slot not found',
                        }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                    # for apointment in appointments:
                    #     appointment_start = timedelta(hours=apointment.TherapyTime_start.hour, minutes=apointment.TherapyTime_start.minute)
                    #     appointment_end = timedelta(hours=apointment.TherapyTime_end.hour, minutes=apointment.TherapyTime_end.minute)

                    # # Calculate new appointment start and end times as timedelta durations
                    #     new_appointment_start = timedelta(hours=therapy_time_start.hour, minutes=therapy_time_start.minute)
                    #     new_appointment_end = new_appointment_start + session_duration

                    # # Check if new appointment overlaps with any existing appointment
                    #     if (new_appointment_start < appointment_end and new_appointment_end > appointment_start):
                    #         return JsonResponse({"error": "Appointment already booked at this time"}, status=409)
            else:
                response = {
                    'status': 'Error',
                    'statusCode': 400,
                    'message': 'Therapist Data not found',
                }        
                return Response(response, status=status.HTTP_404_NOT_FOUND)
                
            provider=Provider.objects.filter(providerId=providerDetail).first()
            service=Service.objects.filter(service_id=service_id).first()
            location=Location.objects.filter(location_id=LocationId).first()

            new_appointment = Appointment1(
                clientId=request.user,
                providerId=provider,
                therapistId=therapist_avail_date.therapist_id,
                serviceId=service,
                appointmentDate=date_appointment,
                TherapyTime_start=therapy_time_start,
                TherapyTime_end=timeslot2,
                LocationId=location,
                status=status_check,
                isconfimed=True
            )
            new_appointment.save()
            if status_check=="confirmed":
                response_data = {
                    'status': 'success',
                    'statusCode': 200,
                    'message':"Your Appointment is Confirmed"
                }
            else:
                response_data = {
                    'status': 'success',
                    'statusCode': 200,
                    'message':"Your Appointment is in waiting list"
                }


            return Response(response_data, status=status.HTTP_200_OK)
    
    @action(detail=False,methods=['post'])
    def delete_user_apointment(self,request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment_id = serializer.validated_data['appointmentId']
            try:
                appointment = Appointment1.objects.get(id=appointment_id)
                appointment.delete()
                response = {
                    'status': 'Success',
                    'statusCode': 200,
                    'message': 'Appointment successfully deleted',
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)
            except Appointment1.DoesNotExist:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Appointment not found',
                }     
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def Get_user_Apointment_detail(self,request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment_id = serializer.validated_data['appointmentId']
            try: 
                data_obj=Appointment1.objects.get(clientId=request.user,id=appointment_id)
                serializer = AppointmentSerializerfetch(data_obj)
        
                response = {
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Request successful',
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                    response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': str(e),
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['post'])
    def Get_user_upcoming_apointment(self,request):
        try:
            data_check=request.data
            date_str=data_check.get("date")
            upcomingappointment=data_check.get("isUpcomingappointment")
            if date_str:
                date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                formatted_date_str = date_obj.strftime('%Y-%m-%d')
                data_obj=Appointment1.objects.filter(clientId=request.user,appointmentDate=formatted_date_str).all()
                serializer = AppointmentSerializerfetch(data_obj,many=True)
                if not serializer.data:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'No appointments found for the given Date',
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                
            elif upcomingappointment:
                t1 = datetime.now()
                time_delta = timedelta(hours=5, minutes=30)
                new_time = t1 + time_delta
                data_obj=Appointment1.objects.filter(clientId=request.user,appointmentDate__gt=new_time).all()
                serializer = AppointmentSerializerfetch(data_obj,many=True)
                if not serializer.data:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'No upcoming appointment is found',
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                data_obj=Appointment1.objects.filter(clientId=request.user).all()
                serializer = AppointmentSerializerfetch(data_obj,many=True)
                if not serializer.data:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'No Appointment found ',
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            response = {
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Request successful',
                    'data': serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)  
        except Exception as e:
            response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Some internal issue',
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)            
    
    @action(detail=True,methods=['post'])
    def reshedule_apointment(self,request):
        try:
            data_check=request.data
            data_new_appointment=data_check.get("resheduleAppointmentDate")
            new_obj = datetime.strptime(data_new_appointment, '%d-%m-%Y')
            data_new_appointment = new_obj.strftime('%Y-%m-%d')
            appointment_id = data_check.get('appointmentId')
            resheduletime=data_check.get('resheduletime')
            appointment = Appointment1.objects.get(clientId=request.user, id=appointment_id)
            therapist_avail_date=therapistAvailability.objects.filter(therapist_id=appointment.therapistId,
                                                                   date=data_new_appointment,Provider=appointment.providerId).first()
            
            try:
                therapy_time_start = datetime.strptime(resheduletime, "%H:%M:%S").time()
            except ValueError:
                return JsonResponse({"error": "Invalid time format for TherapyTime_start"}, status=400)
            
            if therapist_avail_date:
                available=False
                data_avalable_slots=therapist_avail_date.available_slots
                if not data_avalable_slots:
                    return Exception("Therapist slot is not found")

                for time_slot in data_avalable_slots:
                    time1,time2=time_slot.split("-")
                    timeslot1 = datetime.strptime(time1, "%H:%M:%S").time()
                    timeslot2 = datetime.strptime(time2, "%H:%M:%S").time()
                    if therapy_time_start==timeslot1:
                        available=True
                        break
                
                if available:
                    if resheduletime :
                        appointments = Appointment1.objects.filter(
                            appointmentDate=data_new_appointment, 
                            therapistId=therapist_avail_date.therapist_id,isconfimed=True,TherapyTime_start=therapy_time_start)

                    else: 
                        appointments = Appointment1.objects.filter(
                        appointmentDate=data_new_appointment, 
                        therapistId=therapist_avail_date.therapist_id,isconfimed=True,TherapyTime_start=appointment.TherapyTime_start)
                else:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'slots not found ',
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)

                if appointments:
                    print(appointments)
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'slot is already booked',
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                        
                appointment.appointmentDate=data_new_appointment
                if therapy_time_start:
                    appointment.TherapyTime_start=therapy_time_start
                    appointment.TherapyTime_end=timeslot2
                appointment.status="reshudule"
                appointment.save()

                response = {
                        'status': '200',
                        'statusCode': 200,
                        'message': 'your Appointment successfully reschedule',
                    }     
                   

                return Response(response, status=status.HTTP_404_NOT_FOUND)                 
            else:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'please update therapist data',
                    }     
                return Response(response, status=status.HTTP_404_NOT_FOUND)            

        except Exception as e :
            response = {
                    'status': 'Error code',
                    'statusCode': 404,
                    'message': str(e),
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)   
        

class TherapistViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = therapistSerializer




               

 