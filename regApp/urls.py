from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name= 'user_registration'),
    path('signin/', views.LoginAPI.as_view(), name= 'obtain_authtoken'),
    path('change_password/',views.ChangePasswordView.as_view(), name= 'change_password'),
    path('password_reset/',include('django_rest_passwordreset.urls'), name= 'password_reset'),

    path('api-auth',include('rest_framework.urls')),
]