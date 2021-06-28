# DJango imports
from django.urls import path

# Local views
from . import views


app_name = 'users_app'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.LoginUser.as_view(), name='user-login')
]
