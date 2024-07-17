from django.urls import path
from .views import ProviderViewSet,TherapistViewSet,Client_booking_Details



urlpatterns = [
  path('fetch/allprovider',ProviderViewSet.as_view({'get': 'list'}), name='provider-list'),
  path('provide/search',ProviderViewSet.as_view({'post': 'fetch_providers'}), name='provid-fetch'),
  path('provide/<int:pk>',ProviderViewSet.as_view({'get': 'details_provider'}), name='provid-details'),
  path('provide/therapists',ProviderViewSet.as_view({'get': 'details_provider_therapist'}), name='provider-therapist'),
  path('therapist/details',TherapistViewSet.as_view({'get': 'fetch_therapist'}), name='therapist'),
  path('client/booking',Client_booking_Details.as_view({'post': 'create_booking'}), name='client-booking'),
  path('client/booking/details',Client_booking_Details.as_view({'post': 'create_booking1'}), name='client-booking'),
  path('cancel/user/appointment',Client_booking_Details.as_view({'post': 'delete_user_apointment'}), name='delete-appointment'),
  path('user/appointment/detail/byId',Client_booking_Details.as_view({'get': 'Get_user_Apointment_detail'}), name='get-user-detail'),
  path('user/allappointments',Client_booking_Details.as_view({'get': 'Get_user_upcoming_apointment'}), name='get-user-detail'),
  path('user/reshedule/apointment',Client_booking_Details.as_view({'get': 'reshedule_apointment'}), name='reshedule_apointment'),
  # path('reshdule/user/<int:pk>/booking/<int:pk>',Client_booking_Details.as_view({'post': 'create_booking1'}), name='client-booking'),
]