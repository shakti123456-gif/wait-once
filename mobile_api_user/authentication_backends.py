from django.contrib.auth.backends import ModelBackend
from .models import User_mobile

class userlogin(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User_mobile.objects.get(mobile_number=username,password=password)
            return user
        except Exception as e:
            return None


    def get_user(self, user_id):
        try:
            return User_mobile.objects.get(pk=user_id)
        except User_mobile.DoesNotExist:
            return None
