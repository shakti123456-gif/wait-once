from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['mobile_number'] = user.mobileNumber
        # role id 
        return token

class CustomRefreshToken(RefreshToken):
    @classmethod
    def or_user(cls, user):
        token = super().for_user(user)
        token['mobile_number'] = user.mobileNumber
        # role id 
        return token
    


