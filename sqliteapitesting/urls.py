
from django.contrib import admin
from django.urls import path,include
from .Swagger import schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('',include("mobile_api_user.urls")),
    path('api/',include("Client_provider.urls")),
    path('swagger/', schema_view.with_ui('swagger',
                cache_timeout=0), name='schema-swagger-ui')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

