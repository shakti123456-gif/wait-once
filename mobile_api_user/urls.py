from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView

urlpatterns = [
  
    path("", TemplateView.as_view(template_name="home.html")),
    path('user/create',UserRegistrationView.as_view(), name='create_mobile_user'),
    path('user/update-data/',UserUpdateView.as_view()),
    path('user/fetch-details',Fetch_and_update_user.as_view()),
    path('user/login', Loginapi_views_jwt.as_view()),
    path('logout/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='auth_logout'),
    path('terms-conditions/', TemplateView.as_view(template_name='WO_T_C.html'), name='WO_T_C'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy.html'), name='WO_T_C'),
    path('user/children-details', ChildrenListView.as_view(),name="fetch_child_data"),
    path('delay/',show,name="show-error")
]

# urlpatterns = format_suffix_patterns(urlpatterns)
