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
            user = User_mobile.objects.get(mobileNumber=username)
            return user
        except Exception as e:
            return None


    def get_user(self, user_id):
        try:
            return User_mobile.objects.get(pk=user_id)
        except User_mobile.DoesNotExist:
            return None
        



class CustomJWTAuthentication(BaseAuthentication):
    def get_header(self, request):

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        parts = auth_header.split()
        if len(parts) != 4 or parts[0].lower() != 'Userid' or parts[2].lower() != 'token':
            raise AuthenticationFailed('Invalid Authorization header format')
        return parts[1], parts[3]


    def get_raw_token(self, header):
        # Check if the header contains the token
        return header if header else None

    def get_validated_token(self, raw_token):
        # Validate the token here, e.g., check signature, expiry, etc.
        # This method should be implemented according to your validation logic
        # For simplicity, we assume the raw_token is the validated token
        return raw_token

    def get_user(self, validated_token):
        # Retrieve the user based on the validated token
        # This method should be implemented according to your user retrieval logic
        # For simplicity, returning None (should fetch the user from the database)
        return None

    def authenticate(self, request):
        header,some = self.get_header(request)
        print(header,some)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            payload = jwt.decode(raw_token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=["HS256"])
            user_id = payload.get('UserId')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')

        user = self.get_user(validated_token)
        if user is None or user.UserId != user_id:
            raise AuthenticationFailed('Token user mismatch')

        return (user, validated_token)
