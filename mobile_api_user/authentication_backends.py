from django.contrib.auth.backends import ModelBackend
from .models import User_mobile
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt
from rest_framework.authentication import BaseAuthentication

class userlogin(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User_mobile.objects.get(mobileNumber=username,password=password)
            return user
        except Exception as e:
            return None


    def get_user(self, user_id):
        try:
            return User_mobile.objects.get(pk=user_id)
        except User_mobile.DoesNotExist:
            return None
        



