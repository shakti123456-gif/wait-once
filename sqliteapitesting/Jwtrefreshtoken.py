from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
            #  userId = request.headers.get('userId')
            # mobile_id = request.headers.get('mobileNumber')
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            user = User.objects.get(userId=refresh["userId"])
            new_access_token = RefreshToken.for_user(user).access_token
            new_access_token['userId'] = user.userId
            new_access_token['mobile_number'] = user.mobileNumber
            
            return Response({
                'access': str(new_access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
