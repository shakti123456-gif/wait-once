from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # Add custom claims here
        token['mobile_number'] = user.mobile_number
        # Example of an additional field
        return token

class CustomRefreshToken(RefreshToken):
    @classmethod
    def or_user(cls, user):
        token = super().for_user(user)
        # Add custom claims to the refresh token as well if needed
        token['mobile_number'] = user.mobile_number
        token['custom_field'] = 'custom_value'  # Example of an additional field
        return token