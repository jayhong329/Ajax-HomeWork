from django.urls import path, include
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/
    path('', views.index),

    # http://127.0.0.1:8000/travel/
    path('travel/', views.travel),

    # http://127.0.0.1:8000/register/
    path('register/', views.register),


]