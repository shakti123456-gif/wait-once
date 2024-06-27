from mobile_api_user.authentication import JWTAuthentication
from rest_framework import generics
from .models import Provider,Therapist,Service,therapist_service
from .Serializers import ProviderSerializer,therapistSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound



class ProviderListRetrieveView(generics.GenericAPIView):
    serializer_class = ProviderSerializer


    def get_queryset(self):
        userId = self.request.headers.get('userId',None)
        try:
            client_detail = Provider.objects.filter(Client_auth__userId=userId).first()
            caretakers=[]
            if client_detail:
                caretakers = client_detail.Add_Caretaker_Detail.all()
            return caretakers
        except Exception as e:
                print(e)


    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def list(self, request, search ,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, name ,*args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response = {
                'status': 'error',
                'status-code': 404,
                'message': 'Provider  not found',
            }
        
        return Response(response, status=404)


class TherapistListRetrieveView(generics.GenericAPIView):
    queryset = Therapist.objects.all()
    serializer_class = therapistSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self,request,service,*args, **kwargs):
        data_pk=kwargs.get('service')
        therapist = Therapist.objects.get(therapist_id=data_pk)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data
        return Response(serialized_data)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)       
        response = {
                'status': 'error',
                'status-code': 404,
                'message': 'Provider  not found',
            }
        return Response(response, status=404)
 







