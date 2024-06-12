

from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

urlpatterns = [
    path('',home,name='home'),
    path('user/create',UserRegistrationView.as_view(), name='create_mobile_user'),
    path('user/update_data',update_user_data.as_view()),
    path('user/loginjwt', Loginapi_views_jwt.as_view()),
    path('logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='auth_logout'),
    path('service/',fetch_all_Service.as_view(),name="service"),
    path('terms-conditions/', TemplateView.as_view(template_name='WO_T_C.html'), name='WO_T_C'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
