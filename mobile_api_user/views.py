
from rest_framework import generics, status 
from .models import User_mobile,Fix_time
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializer import LoginAPIView ,User_mobile_serialize,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from .jwt_token import *
from rest_framework.permissions import AllowAny
from django.db.models import Q
import pytz
from datetime import datetime ,timedelta

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = User_mobile_serialize
    queryset = User_mobile.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                response_data = {
                    "status": "success",
                    "code": 201,
                    "message": "User successfully created"
                    # "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                details = [{'field': key, 'issue': error[0]} for key, error in serializer.errors.items()]
                response_data = {
                    "status": "error",
                    "code": 400,
                    "message": "Bad Request",
                    "details": details
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

class update_user_data(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, number):
        try:
            return User_mobile.objects.get(MobileNumber=number)
        except User_mobile.DoesNotExist:
            raise Http404("User not exist ")

    def put(self,request, format=None):
        data_item=request.data
        number=data_item.get('MobileNumber',None)
        data_obj = self.get_object(number)

        serializer = User_mobile_serialize(data_obj, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                    'status': 'success',
                    'code': 200,
                    'message': 'Password Successfully updated',
                }
            return Response(response, status=status.HTTP_200_OK)
        else:
            details = [{'field': key, 'issue': error[0]} for key, error in serializer.errors.items()]
            response = {
                    'status': 'error',
                    'code': 401,
                    'message': 'Invalid credentials',
                    'details': [{'field': 'username', 'issue': 'Invalid username or password'}]
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class Loginapi_views_jwt(APIView):
    serializer_class = LoginAPIView

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            Mobile_number=request.headers.get('MobileNumber')
            user_name = serializer.validated_data['Username']
            password = serializer.validated_data['Password']
            
            if not user_name:
                user_name=Mobile_number
            user_stat = User_mobile.objects.filter(
                            (Q(MobileNumber=str(user_name)) | Q(EmailAddress=str(user_name))) & Q(password=password)
                        ).first()
            
            if user_stat:
                refresh = CustomRefreshToken.for_user(user_stat)
                access = CustomAccessToken.for_user(user_stat)
                
                data = {
                    'refresh': str(refresh),
                    'access': str(access),
                    'id': user_stat.UserId,
                    'name': user_stat.FirstName,
                    'email': user_stat.EmailAddress,
                    'Created_At': Fix_time(user_stat.Created_At)
                }
                response = {
                    'status': 'success',
                    'code': 200,
                    'message': 'Request successful',
                    'data': data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 'error',
                    'code': 401,
                    'message': 'Invalid credentials',
                    'details': [{'field': 'username', 'issue': 'Invalid username or password'}]
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        details = [{'field': key, 'issue': error[0]} for key, error in serializer.errors.items()]
        response = {
                'status': 'error',
                'code': 400,
                'message': 'Bad Request',
                'details': details
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class User_book_apointment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        pass

class UserMobileListAPIView(generics.ListAPIView):
    queryset = User_mobile.objects.all()
    # serializer_class = UserMobileSerializer

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Referse token is deleted "}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"you already deleted this token"}, status=status.HTTP_200_OK)


class fetch_all_Service(generics.ListAPIView):
    pass

class CustomLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


