
from rest_framework import generics, status 
from .models import User_mobile
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404,HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .Serializer import LoginAPIView ,User_mobile_serialize,UserMobileSerializer
from rest_framework_simplejwt.tokens import RefreshToken 
from .jwt_token import *
from django.db.models import Q
from .authentication_backends import CustomJWTAuthentication
from .authentication import JWTAuthentication
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = User_mobile_serialize
    queryset = User_mobile.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                try:
                    self.perform_create(serializer)
                except Exception as e:
                    print(e)

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
    
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
   

    def get_object(self, number):
        try:
            return User_mobile.objects.get(mobileNumber=number)
        except User_mobile.DoesNotExist:
            response={
                'status': 'error',
                'status-code': 401,
                'message': 'Invalid credentials',
            }
            raise Http404(response)
        
    def get(self,request,*args, **kwargs):
        try:
            user_Id = request.headers.get('userID')
            if user_Id is not None:
                user_object = User_mobile.objects.get(userId=user_Id)
                serializer = UserMobileSerializer(user_object)
            else:
                raise Exception ("User is not valid")
            return Response(serializer.data)
        except User_mobile.DoesNotExist:
            response = {
                'status': 'error',
                'status-code': 404,
                'message': 'User not found',
            }
            return Response(response, status=404)
        except Exception as e:
            response = {
                'status': 'error',
                'status-code': 400,
                'message': str(e),
            }
            return Response(response, status=400)


    def put(self,request, format=None):
        data_item=request.data
        number=data_item.get('mobileNumber',None)
        data_obj = self.get_object(number)

        serializer = User_mobile_serialize(data_obj, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Password Successfully updated',
                }
            return Response(response, status=status.HTTP_200_OK)
        else:
            details = [{'field': key, 'issue': error[0]} for key, error in serializer.errors.items()]
            response = {
                    'status': 'error',
                    'statusCode': 401,
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
            user_name = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            if not user_name:
                user_name=Mobile_number
            user_stat = User_mobile.objects.filter(
                            (Q(mobileNumber=str(user_name)) | Q(email=str(user_name))) & Q(password=password)
                        ).first()
            
            if user_stat:
                refresh = CustomRefreshToken.for_user(user_stat)
                access = CustomAccessToken.for_user(user_stat)
                
                data = {
                    'refreshToken': str(refresh),
                    'accessToken': str(access),
                    'userId': user_stat.userId,
                    'name': user_stat.firstName,
                    'email': user_stat.email
                }
                response = {
                    'status': 'success',
                    'statusCode': 200,
                    'message': 'Request successful',
                    'data': data
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'status': 'error',
                    'statusCode': 401,
                    'message': 'Invalid credentials',
                    'details': [{'field': 'username', 'issue': 'Invalid username or password'}]
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        details = [{'field': key, 'issue': error[0]} for key, error in serializer.errors.items()]
        response = {
                'status': 'error',
                'statusCode': 400,
                'message': 'Bad Request',
                'details': details
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class User_book_apointment(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_mobiles = User_mobile.objects.all()
        print(f"Retrieved user mobiles: {user_mobiles}")
        return Response({'message': 'Appointment booked successfully'}, status=status.HTTP_200_OK)
    

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

def api_hit(request):
    import requests

    url = "https://api.au1.cliniko.com/v1/appointment_types"

    query = {
        "order": "asc",
        "page": "0",
        "per_page": "1",
        "q[]": "string",
        "sort": "created_at:desc"
        }

    response = requests.get(url, params=query, auth=('<username>','<password>'))

    data = response.json()
    print(data)
    return HttpResponse(data)






