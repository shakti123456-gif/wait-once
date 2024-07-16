
from rest_framework import generics, status
from .models import User_mobile,Client_details_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404,HttpResponse
from rest_framework.permissions import IsAuthenticated
from .Serializer import LoginAPIView ,UserMobileSerializer,ClientDetailSerializer,ClientSubSerializer,UserMobileSerializerfetch
from rest_framework_simplejwt.tokens import RefreshToken 
from .jwt_token import *
from django.db.models import Q
from .authentication import JWTAuthentication
from .task import add
from django.http import JsonResponse
from rest_framework.decorators import api_view

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = ClientDetailSerializer
    queryset = Client_details_view.objects.all()
    
    def create(self, request, *args, **kwargs):
        client_auth_data = request.data.pop('ClientAuth', None)
        if not client_auth_data:
            response = {
                'status': 'error',
                'status-code': 400,
                'message': 'ClientAuth data is required'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        client_auth_serializer = UserMobileSerializer(data=client_auth_data)
        add_caretaker_detail = []

        if client_auth_data.get("signingAs") == "Parent":
            add_caretaker_data = request.data.pop('addChildren', None)
            if add_caretaker_data is None:
                response = {
                    'status': 'error',
                    'status-code': 400,
                    'message': 'Please add Caretaker details',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            add_caretaker_serializer = ClientSubSerializer(data=add_caretaker_data, many=True)
            if not add_caretaker_serializer.is_valid():
                details = [
                    {'field': key, 'issue': error[0]}
                    for error_dict in add_caretaker_serializer.errors
                    for key, error in error_dict.items()
                ]
                response = {
                    'status': 'error',
                    'status-code': 400,
                    'message': 'Invalid Caretaker details',
                    'details': details
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if not client_auth_serializer.is_valid():
            details = [
                {'field': key, 'issue': error[0]}
                for key, error in client_auth_serializer.errors.items()
            ]
            response_data = {
                "status": "error",
                "code": 400,
                "message": "Bad Request",
                "details": details
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if client_auth_data.get("signingAs") == "Parent":
                add_caretaker_detail = add_caretaker_serializer.save()

            client_auth = client_auth_serializer.save()
            serializer.save(Client_auth=client_auth, addChildren=add_caretaker_detail)

            response = {
                'status': 'success',
                'status-code': 201,
                'message': 'User created successfully'
            }
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class Fetch_and_update_user(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self,**kwargs):
        try:
            phonenumber= kwargs.get("number",None)
            if  phonenumber is None:
                raise Exception("")
            return User_mobile.objects.get(mobileNumber=phonenumber)
        except User_mobile.DoesNotExist:
            response={
                'status': 'error',
                'status-code': 401,
                'message': 'Invalid credentials',
            }
            raise Http404(response)
        
    def get(self,request,*args, **kwargs):
        try:
            user_Id = request.headers.get('userId',None)
            if user_Id is None:
                response = {
                'status': 'error',
                'status-code': 404,
                'message': 'Please pass userId in header',
                }
            user_object = User_mobile.objects.get(userId=user_Id)
            data_obj=Client_details_view.objects.get(Client_auth=user_object)
            percentage=data_obj.percentage_empty_fields()
            serializer = UserMobileSerializerfetch(user_object)
            response_data = serializer.data
            percentage = round(percentage, 2)
            response_data['percentage']=percentage
            return Response(response_data)
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
                    'mobileNumber': user_stat.mobileNumber
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
    

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message":"Referse token is deleted "}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"you already deleted this token"}, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    def put(self, request, *args, **kwargs):
        try:
            user_name=request.data.get("username")
            password=request.data.get("newpassword")
            user_stat = User_mobile.objects.filter(
                            (Q(mobileNumber=str(user_name)) | Q(email=str(user_name)))
                        ).first()
            if not user_stat:
                response = {
                'status': 'error',
                'statusCode': 400,
                'message': 'Requested user is not exist',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            user_stat.password=password
            user_stat.save()
            response = {
                'status': 'Success',
                'statusCode': 200,
                'message': 'password was Successfully updated',
                }
            return Response(response, status=status.HTTP_200_OK)
        
        except Exception as e:
            response = {
                'status': 'error',
                'statusCode': 400,
                'message': 'Internal server error occured',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
    
class ChildrenListView(generics.ListAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class=ClientSubSerializer

    def get_queryset(self):
        userId = self.request.headers.get('userId',None)
        try:
            client_detail = Client_details_view.objects.filter(Client_auth__userId=userId).first()
            caretakers=[]
            if client_detail:
                caretakers = client_detail.Add_Caretaker_Detail.all()
            return caretakers
        except Exception as e:
                print(e)

    def list(self, request):
        queryset = self.get_queryset()
        if not queryset:
            response = {
                'status': 'error',
                'statusCode': 200,
                'message': 'user doestnot have children details',
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_application_configuration(request):
    res= {
        "status": "success",
        "statusCode": 200,
        "message": "Request successful",
        "data": {
            "quote": {
            "message": "Doctors, have a big responsibility to bring smiles to the faces of suffering humanity.",
            "author": "Narayana Murthy"
            }
        }
    }
    return JsonResponse(res)

























def show(request):
    pass