from django.urls import path
from .views import LoginWithOTP, ValidateOTP, UserProfile


urlpatterns = [
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('user-info/', UserProfile.as_view(), name='user-profile'),
]
