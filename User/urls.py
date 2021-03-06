from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='user-registration'),
    path('login/', login, name='user-login'),
    path('logout/', logout, name='user-logout'),
    path('profile/', profile, name='user-profile'),
]
