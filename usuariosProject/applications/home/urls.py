# DJango imports
from django.urls import path

# Local views
from . import views


app_name = 'home_app'

urlpatterns = [
    path('panel/', views.HomePage.as_view(), name='panel')
]
