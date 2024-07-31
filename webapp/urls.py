





from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [

    path("", TemplateView.as_view(template_name="home.html")),
    path('provider',ProviderViewSet.as_view({'get': 'details_provider'}), name='provid-details'),
]