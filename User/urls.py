from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='user-registration'),
    path('login/', login, name='user-login'),
    path('logout/', logout, name='user-logout'),
    path('profile/', profile, name='user-profile'),
    path('profileEdit/', profileEdit, name='user-profileEdit'),
    path('profilePicEdit/', profilePicEdit, name='user-profilePicEdit'),
    path('aadharPicEdit/', aadharPicEdit, name='user-aadharPicEdit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
