from django.urls import path
from .views import ProviderViewSet,TherapistViewSet,Client_booking_Details



urlpatterns = [
  path('fetch/allprovider',ProviderViewSet.as_view({'get': 'list'}), name='provider-list'),
  path('provide/search',ProviderViewSet.as_view({'post': 'fetch_providers'}), name='provid-fetch'),
  path('provide/<int:pk>',ProviderViewSet.as_view({'get': 'details_provider'}), name='provid-details'),
  path('provide/therapists',ProviderViewSet.as_view({'get': 'details_provider_therapist'}), name='provider-therapist'),
  path('therapist/details',TherapistViewSet.as_view({'get': 'fetch_therapist'}), name='therapist'),
  path('client/booking',Client_booking_Details.as_view({'post': 'create_booking'}), name='client-booking'),

]