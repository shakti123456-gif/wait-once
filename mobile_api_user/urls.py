

from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

urlpatterns = [
  
    path("", TemplateView.as_view(template_name="home.html")),
    path('user/create',UserRegistrationView.as_view(), name='create_mobile_user'),
    path('user/update-data',update_user_data.as_view()),
    path('user/fetch-details',update_user_data.as_view()),
    path('user/login', Loginapi_views_jwt.as_view()),
    path('logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='auth_logout'),
    path('terms-conditions/', TemplateView.as_view(template_name='WO_T_C.html'), name='WO_T_C'),
    path('custom-api-auth/', User_book_apointment.as_view(), name='no_module'),
    path('api_hit/',api_hit,name="api-hit")
]

# urlpatterns = format_suffix_patterns(urlpatterns)
