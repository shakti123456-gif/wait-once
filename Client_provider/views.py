from mobile_api_user.authentication import JWTAuthentication
from rest_framework import generics
from .models import Provider,Therapist,Service,therapist_service
from .Serializers import ProviderSerializer,therapistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, viewsets
from rest_framework.decorators import action




class ProviderViewSet(viewsets.ModelViewSet):

    def list(self, request):
        queryset = Provider.objects.all()
        serializer = ProviderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Provider.objects.filter(pk=pk).first()
        serializer = ProviderSerializer(queryset)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def therapist(self, request, pk=None):
        provider = Provider.objects.filter(pk=pk).first()
        # Assuming Therapist is related to Provider somehow
        therapists = provider.therapists.all()
        serializer = TherapistSerializer(therapists, many=True)
        return Response(serializer.data)

    pass








