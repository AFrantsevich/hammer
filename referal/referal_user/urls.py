from django.urls import path
from .views import login_request, authenticate_user, user_info, get_code
from django.contrib.auth.views import LogoutView


app_name = 'referal_user'


urlpatterns = [
    path('login/', login_request, name='login'),
    path('auth/', authenticate_user, name='auth'),
    path('user_info/', user_info, name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getcode/', get_code, name='get_code'),
]



