from django.urls import path
from .views import ProviderListRetrieveView,TherapistListRetrieveView



urlpatterns = [
  path('provide/',ProviderListRetrieveView.as_view(), name='user-list'),
  path('provide/<int:pk>/', ProviderListRetrieveView.as_view(), name='provider-detail'),
  path('therapist',TherapistListRetrieveView.as_view(), name='therapist'),
  path('therapist/<int:pk>/', TherapistListRetrieveView.as_view(), name='therapist'),

]