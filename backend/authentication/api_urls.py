from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import api_views

urlpatterns = [
    path('token/', api_views.LoginView.as_view(), name='api_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('me/', api_views.MeView.as_view(), name='api_me'),
    path('change-password/', api_views.ChangePasswordView.as_view(), name='api_change_password'),
]
