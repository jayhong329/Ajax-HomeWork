from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/api/
    path('', views.index ),

    # http://127.0.0.1:8000/api/travel/
    path('travel/', views.travel ),

    # http://127.0.0.1:8000/api/register/
    path('register/', views.register ),
    # http://127.0.0.1:8000/api/checkname/
    path('checkname/', views.checkname ),
    # http://127.0.0.1:8000/api/checkemail/
    path('checkemail/', views.checkemail ),
    # http://127.0.0.1:8000/api/checkpassword/
    path('checkpassword/', views.checkpassword ),
]