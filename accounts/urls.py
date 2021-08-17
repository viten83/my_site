from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token, obtain_jwt_token
from .views import UserRegistrationAPIView

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view()),
    path('token-login/', obtain_jwt_token),
    path('token-refresh/', refresh_jwt_token),
    path('token-verify/', verify_jwt_token),
]