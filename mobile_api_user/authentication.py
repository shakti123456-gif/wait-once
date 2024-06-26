import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import User_mobile


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'bearer':
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')
        try:
            response = {
                    'status': 'error',
                    'statusCode': 403
                }
            token = auth[1]
            userId = request.headers.get('userID')
            mobile_id = request.headers.get('mobileNumber')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            jwt_user_id=payload.get('userId')
            if str(userId) != str(jwt_user_id):
                response['message']='Aceess token is not match with UserID'
                raise exceptions.AuthenticationFailed(response)
            
            if payload.get('mobile_number') != mobile_id:
                response['message']='Aceess token is not match with mobile_number'
                raise exceptions.AuthenticationFailed(response)
            try:
                user = User_mobile.objects.get(userId=userId)
            except User_mobile.DoesNotExist:
                response['message']='User not found'
                raise exceptions.AuthenticationFailed(response)

        except jwt.ExpiredSignatureError:
            response['message']='Token has expired'
            raise exceptions.AuthenticationFailed(response)
        except jwt.InvalidTokenError:
            response['message']='Invalid token'
            raise exceptions.AuthenticationFailed(response)

        return (user, token)
