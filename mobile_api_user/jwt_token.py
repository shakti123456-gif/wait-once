from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['mobile_number'] = user.mobileNumber
        return token

class CustomRefreshToken(RefreshToken):
    @classmethod
    def or_user(cls, user):
        token = super().for_user(user)
        token['mobile_number'] = user.mobileNumber
        token['custom_field'] = 'custom_value' 
        return token
    


