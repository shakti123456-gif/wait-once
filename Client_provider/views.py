from mobile_api_user.authentication import JWTAuthentication
from .models import Provider,Therapist,Service,therapist_service,Location,therapistAvailability,\
    Appointment,Appointment1,clientPrebookAppointments,ReoccureAppointments
from .Serializers import ProviderSerializer,therapistSerializer,ProviderSerializerdetail,LocationSerializerdetail,ServiceSerializerdetail,\
    AppointmentSerializer,AppointmentSerializerfetch,TherapistAvailSerializer ,RescheduleAppointmentSerializer,ServiceSerializerdetailAppointment,\
    reoccureAppointment
    
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from datetime import datetime, timedelta
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta


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
            queryset = queryset.filter(pin=pin_code)
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
            serialized_data['therapists'] = therapist_serializer.data
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
        providerId=request.headers.get("providerId",None)
        therapistId=request.headers.get("therapistId",None)
    
        if not providerId or not therapistId:
            raise Exception("providerId  and TherapistId should present in headers")
        try:
            provider_data=Provider.objects.filter(providerId=providerId).first()
            data = provider_data.get_therapist_services(therapistId)
            service_serializer = ServiceSerializerdetail(data, many=True)
            if not service_serializer.data:
                response = {
                'status': 'error',
                'statusCode': 404,
                'message': 'service data not found',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)  

            response = {
                'status': 'success',
                'statusCode': 200,
                'message': 'Request successful',
                'data': service_serializer.data
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
    
    @action(detail=False, methods=['get', 'post'])
    def details_locations(self, request):
        if request.method == 'GET':
            Providerid = request.headers.get("Providerid", None)
            provider_data=Provider.objects.filter(providerId=Providerid).first()
            if not provider_data:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Provider user Id is not exit',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            locations_data=provider_data.Provider_locations_add
            location_serializer = LocationSerializerdetail(locations_data, many=True)
            response = {
                'status': 'success',
                'statusCode': 200,
                'message': 'Request successful',
                'data': location_serializer.data
                }
            return Response(response, status=status.HTTP_200_OK) 
        
        if request.method == 'POST':
            # i want add data
            return Response({'message': 'POST request received'})
        
    @action(detail=False, methods=['get', 'post'])
    def details_employee(self, request):
        if request.method == 'GET':
            Providerid = request.headers.get("Providerid", None)
            provider_data=Provider.objects.filter(providerId=Providerid).first()
            if not provider_data:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'Provider user Id is not exit',
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            locations_data=provider_data.Provider_locations_add
            location_serializer = LocationSerializerdetail(locations_data, many=True)
            response = {
                'status': 'success',
                'statusCode': 200,
                'message': 'Request successful',
                'data': location_serializer.data
                }
            return Response(response, status=status.HTTP_200_OK) 
        
        if request.method == 'POST':
            # i want add data
            return Response({'message': 'POST request received'})


class TherapistViewSet(viewsets.ModelViewSet):
    serializer_class = therapistSerializer

    def get_queryset(self, therapist_id=None):
        try:
            queryset = Therapist.objects.get(therapist_id=therapist_id)
            data_therapist=therapist_service.objects.filter(Therapist_Name=queryset)
            details_service=[e.service_Name.service_id for e in data_therapist]
            service_data=Service.objects.filter(service_id__in=details_service)
            providers_data = Provider.objects.filter(therapistServicemap__in=data_therapist).distinct()

            data={
                "TherapistData":queryset,
                "serviceData":service_data,
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
        
        service_serializer = ServiceSerializerdetail(data.get("serviceData", None), many=True)
        therapist_data_serializer = therapistSerializer(data.get("TherapistData", None))
        provider_data_serializer = ProviderSerializer(data.get("providers", None), many=True)

        response_data = {
                'status': 'success',
                'statusCode': 200,
                'data': {
                    'therapist': therapist_data_serializer.data,
                    'services': service_serializer.data,
                    'providers': provider_data_serializer.data,
                }
            }
        return Response(response_data, status=status.HTTP_200_OK)


    @action(detail=True,methods=['get'])
    def therapist_availablity(self, request, pk=None):
        try:
            availablityDate1=request.headers.get("availablityDate",None)
            data1={
                "availablityDate":availablityDate1
            }
            serializer = TherapistAvailSerializer(data=data1)
            if serializer.is_valid():
                data_avail = serializer.validated_data.get("availablityDate")
                therapistId=request.headers.get("therapistId",None)
                providerId=request.headers.get("providerId",None)
                if therapistId:
                    therapist_data = therapistAvailability.objects.get(therapist_id__therapist_id=therapistId,date=data_avail,Provider__providerId=providerId)
                else:
                    response_data = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': "provide therapistId in headers"
                    }
                    return Response(response_data, status=status.HTTP_404_NOT_FOUND)
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
                        "therapistId":therapistId,
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
                    'message': "Therapist id not found or therapist data is not updated"
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
            
            if therapist_avail_date:
                appointments = Appointment.objects.filter(
                        appointmentDate=date_appointment, 
                        therapistId=therapist_avail_date.therapist_id.therapist_id,isConfirmed=True)
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
                isConfirmed=True
            )
            new_appointment.save()
        
        return HttpResponse("Appointment booking is done ")
    
    @action(detail=True,methods=['post'])
    def create_booking1(self,request,pk=None):
        try:
            data=request.data
            therapist_avail=data.get("therapist",None)
            date_appointment=data.get("appointmentDate",None)
            childDetail=data.get("children",None)
            therapy_time_start = data.get("therapyTimeStart",None)
            providerDetail=data.get("provider",None)
            service_id=data.get("service",None)
            session_time=data.get("sessionTime",None)
            LocationId=data.get("LocationId",None)

            try:
                date_appointment = datetime.strptime(date_appointment, '%d-%m-%Y').strftime('%Y-%m-%d')
            except:
                return JsonResponse({"error": "please enter format day/month/year"}, status=400)
            try:
                therapy_time_start = datetime.strptime(therapy_time_start, "%H:%M:%S").time()
            except ValueError:
                return JsonResponse({"error": "Invalid time format for TherapyTime_start"}, status=400)
            
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
                                therapistData=therapist_avail_date.therapist_id,TherapyTime_start=timeslot1)

                        if appointments:
                            for appoint in appointments:
                                if appoint.clientData.userId==request.user.userId or  childDetail:
                                    response = {
                                        'status': 'error',
                                        'statusCode': 404,
                                        'message': 'you are already booked this slot',
                                    }
                                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                            status_check="waiting" 
                    else:
                        response = {
                                'status': 'error',
                                'statusCode': 404,
                                'message': 'slot not found',
                            }
                        return Response(response, status=status.HTTP_404_NOT_FOUND)
                        
                else:
                    response = {
                        'status': 'error',
                        'statusCode': 400,
                        'message': 'Therapist Data not found with particular provider or therapist time is not updated',
                    }        
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                    
                provider=Provider.objects.filter(providerId=providerDetail).first()
                service=Service.objects.filter(service_id=service_id).first()
                location=Location.objects.filter(location_id=LocationId).first()
                new_appointment = Appointment1(
                    clientData=request.user,
                    providerData=provider,
                    therapistData=therapist_avail_date.therapist_id,
                    serviceData=service,
                    appointmentDate=date_appointment,
                    TherapyTime_start=therapy_time_start,
                    TherapyTime_end=timeslot2,
                    locationData=location,
                    status=status_check,
                    isConfirmed = True if status_check == "confirmed" else False
                )
                new_appointment.save()
                if status_check=="confirmed":
                    response_data = {
                        'status': 'success',
                        'statusCode': 200,
                        'message':"your appointment is confirmed"
                    }
                else:
                    response_data = {
                        'status': 'success',
                        'statusCode': 200,
                        'message':"Your Appointment is in waiting list"
                    }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                        'status': 'error',
                        'statusCode': 404,
                        'message':str(e)
                    }

            return Response(response_data, status=status.HTTP_200_OK)

    
    @action(detail=True,methods=['post'])
    def delete_user_apointment(self,request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment_id = serializer.validated_data['appointmentId']
            try:
                appointment = Appointment1.objects.get(id=appointment_id)
                if appointment.status=="confirmed":
                    appointment_second_record = Appointment1.objects.filter(
                        appointmentDate=appointment.appointmentDate,
                        TherapyTime_start=appointment.TherapyTime_start
                        ).order_by('createdAt')
                    if appointment_second_record.count() >1:
                        second_record = appointment_second_record[1]
                        second_record.status = "confirmed"
                        second_record.isConfirmed = True
                        second_record.save()
                appointment.delete()
                response = {
                    'status': 'Success',
                    'statusCode': 200,
                    'message': 'Appointment successfully deleted',
                }
                return Response(response,status=status.HTTP_204_NO_CONTENT)
            except Exception as e :
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': str(e),
                }     
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,methods=['get'])
    def Get_user_Apointment_detail(self,request):
        data_pd_id=request.headers.get("appointmentId","None")
        if not data_pd_id:
            return Response({'error': 'appointmentId not found in headers'}, status=status.HTTP_400_BAD_REQUEST)
        data_id={
            'appointmentId':data_pd_id
        }
        serializer = AppointmentSerializer(data=data_id)
        if serializer.is_valid():
            appointment_id = serializer.validated_data['appointmentId']
            try: 
                data_obj=Appointment1.objects.get(clientData=request.user,id=appointment_id)
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
                    'message': 'ApointmentId  doest not Exist',
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,methods=['post'])
    def Get_user_upcoming_apointment(self,request):
        try:
            data_check=request.data
            date_str=request.headers.get("date",None)
            upcomingappointment=data_check.get("isUpcomingappointment")
            if date_str:
                try:
                    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                    formatted_date_str = date_obj.strftime('%Y-%m-%d')
                except Exception as e:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'follow date and time  in this format %d-%m-%Y',
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                data_obj=Appointment1.objects.filter(clientData=request.user,appointmentDate=formatted_date_str).all()
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
                data_obj=Appointment1.objects.filter(clientData=request.user,appointmentDate__gt=new_time).all()
                serializer = AppointmentSerializerfetch(data_obj,many=True)
                if not serializer.data:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'No upcoming appointment is found',
                    }
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                data_obj=Appointment1.objects.filter(clientData=request.user).all()
                serializer = AppointmentSerializerfetch(data_obj,many=True)
                if not serializer.data:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'No Appointment found',
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
                    'message': str(e),
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)            
    
    @action(detail=True,methods=['post'])
    def reshedule_apointment(self,request):
        try:
            serializer = RescheduleAppointmentSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                appointment_id = validated_data['appointmentId']
                reschedule_date = validated_data['rescheduleAppointmentDate']
                resheduletime = validated_data['rescheduleTime']
            else:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'data': serializer.errors,
                    }     
                return Response(response, status=status.HTTP_404_NOT_FOUND)            
            
            appointment = Appointment1.objects.get(clientData=request.user, id=appointment_id)
            therapist_avail_date=therapistAvailability.objects.filter(therapist_id=appointment.therapistData,
                                                                   date=reschedule_date,Provider=appointment.providerData).first()
            try:
                therapy_time_start = resheduletime
            except ValueError:
                return JsonResponse({"error": "Invalid time format for TherapyTime_start"})
            
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
                            appointmentDate=reschedule_date, 
                            therapistData=therapist_avail_date.therapist_id,isConfirmed=True,TherapyTime_start=therapy_time_start)

                    else: 
                        appointments = Appointment1.objects.filter(
                        appointmentDate=reschedule_date, 
                        therapistData=therapist_avail_date.therapist_id,isConfirmed=True,TherapyTime_start=appointment.TherapyTime_start)
                else:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'slots not found',
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)

                if appointments:
                    response = {
                        'status': 'error',
                        'statusCode': 404,
                        'message': 'slot is already booked',
                    }     
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                        
                appointment.appointmentDate=reschedule_date
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
                
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': 'please update therapist data',
                    }     
                return Response(response, status=status.HTTP_404_NOT_FOUND)            

        except Exception as e :
            response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': str(e),
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True,methods=['get'])
    def userServiceDetail(self,request):
        try:
            serviceData=Appointment1.objects.filter(clientData=request.user).values("serviceData").distinct()
            if not serviceData:
                raise Exception("service data not  found")
            serviceDataId=[service['serviceData'] for service in serviceData]
            dataService=Service.objects.filter(service_id__in=serviceDataId)
            serviceSerializer=ServiceSerializerdetailAppointment(dataService,many=True)
            response = {
                        'status': 'success',
                        'statusCode': 200,
                        'message': 'request Successfull',
                        'data':serviceSerializer.data
                    }     
                    
            return Response(response, status=status.HTTP_200_OK)
        except Exception as  e :
            response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': str(e),
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True,methods=['post'])
    def userServiceTherapist(self,request):
        try:
            serviceId=request.headers.get("serviceId")
            if not serviceId:
                raise Exception("please add service id in headers")
            therapistData=Appointment1.objects.filter(clientData=request.user,serviceData__service_id=serviceId).values('therapistData').distinct()
            if not therapistData:
                raise Exception("therapist data is not found")
            therapistDataId=[therapist['therapistData'] for therapist in therapistData]
            dataTherapist=Therapist.objects.filter(therapist_id__in=therapistDataId).all()
            serviceSerializer=therapistSerializer(dataTherapist,many=True)
            response = {
                        'status': 'success',
                        'statusCode': 200,
                        'message': 'request successfull',
                        'data':serviceSerializer.data
                    }   
            return Response(response, status=status.HTTP_200_OK)
           
        except Exception as  e :
            response = {
                    'status': 'error',
                    'statusCode': 404,
                    'message': str(e),
                    }     
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True,methods=['post'])
    def reoccurAppointment(self,request):
        try:
            Serializer=reoccureAppointment(data=request.data)
            if Serializer.is_valid():
                validated_data = Serializer.validated_data
                therapistId = validated_data.get("therapistId", None)
                startDate = validated_data.get("startDate", None)
                endDate = validated_data.get("endDate", None)
                providerId = validated_data.get("providerId", None)
                serviceId = validated_data.get("serviceId", None)
                therapyTimeStart = validated_data.get("therapyTimeStart", None)
                locationId = validated_data.get("locationId", None)
                appointmentType = validated_data.get("appointmentType", None)
                specific_weekdays = []
                current_date=startDate
                end_date=endDate
                if str(appointmentType).lower() == "daily":
                    while current_date <= end_date:
                        specific_weekdays.append(current_date)
                        current_date += timedelta(days=1)

                elif str(appointmentType).lower() == "fortnightly":
                    while current_date <= end_date:
                        specific_weekdays.append(current_date)
                        current_date += timedelta(weeks=2)
            
                elif str(appointmentType).lower() == "weekly":
                    target_weekday = current_date.weekday()
                    while current_date <= end_date:
                        if current_date.weekday() == target_weekday:
                            specific_weekdays.append(current_date)
                        current_date += timedelta(days=1)
                
                elif str(appointmentType).lower() == "monthly":
                    while current_date <= end_date:
                        specific_weekdays.append(current_date)
                        current_date += relativedelta(months=1)
                if not specific_weekdays:
                    raise Exception("we donot find any  dates")    
                providerDetails_data = Provider.objects.get(providerId=providerId)
                therapist_data = Therapist.objects.get(therapist_id=therapistId)
                location_data = Location.objects.get(location_id=locationId)
                service_data = Service.objects.get(service_id=serviceId)
                person, created = clientPrebookAppointments.objects.get_or_create(
                        clientDetail=request.user,
                        therapistDetails=therapist_data,
                        providerDetails=providerDetails_data,
                        serviceData=service_data,
                        startdate=startDate,
                        endDate=endDate,
                        locationData=location_data,
                        appointmentType=appointmentType,
                        therapySlot=therapyTimeStart
                    )
                if person and not created:
                    raise Exception("we already accept your request")
            else:
                response = {
                    'status': 'Error',
                    'statusCode': 404,
                    'message': 'Bad request',
                    'data': Serializer.errors
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
                
            # list_of_appointments = []
            # therapy_time_start = datetime.strptime(therapyTimeStart, "%H:%M:%S").time()

            # for date in specific_weekdays:
            #     therapy_time_end = (datetime.combine(datetime.today(), therapy_time_start) + timedelta(minutes=30)).time()
            #     appointment = ReoccureAppointments(
            #             clientData=request.user,
            #             providerData=providerDetails_data,
            #             therapistData=therapist_data,
            #             serviceData=service_data,
            #             appointmentDate=date,
            #             locationData=location_data,
            #             TherapyTime_start=therapy_time_start,
            #             TherapyTime_end=therapy_time_end,
            #             status='waiting',
            #             isconfimed=False,
            #             reoccurAppointmentDetail=client_prebook
            #         )
            #     list_of_appointments.append(appointment)
            # ReoccureAppointments.objects.bulk_create(list_of_appointments)
            response = {
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Request successfully accepted, please wait provider let you know'
                }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 404,
                'message': str(e),
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    def RecurringApointmentConflictCheck(self,request):
        try:
            id=request.headers.get("id",None)
            data=clientPrebookAppointments.objects.filter(clientPreId=id,clientDetail=request.user).first()
            Appointment1_data_check=Appointment1.objects.all()
            therapistavail_data =therapistAvailability.objects.all()
            specific_weekdays = []
            current_date=data.startDate
            end_date=startDate
            if appointmentType == "daily":
                while current_date <= end_date:
                    specific_weekdays.append(current_date)
                    current_date += timedelta(days=1)

            elif appointmentType == "fortnightly":
                while current_date <= end_date:
                        specific_weekdays.append(current_date)
                        current_date += timedelta(weeks=2)
            
            elif appointmentType == "weekly":
                target_weekday = current_date.weekday()
                while current_date <= end_date:
                    if current_date.weekday() == target_weekday:
                        specific_weekdays.append(current_date)
                        current_date += timedelta(days=1)
                
            elif appointmentType == "monthly":
                while current_date <= end_date:
                    specific_weekdays.append(current_date)
                    current_date += relativedelta(months=1)
            if not specific_weekdays:
                raise Exception("we donot find any  dates")    

        except  Exception as e:
            print(e)







        





               

 