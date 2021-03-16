from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='start-home'),
    path('about/', about, name='start-about'),
    path('contact/', contact, name='start-contact'),
]
