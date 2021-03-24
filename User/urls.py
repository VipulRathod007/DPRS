from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', register, name='user-registration'),
    path('hospitalRegister/', hospitalRegister, name='hospital-registration'),
    path('ngoRegister/', ngoRegister, name='ngo-registration'),
    path('login/', login, name='user-login'),
    path('hospitalLogin/', login, name='hospital-login'),
    path('ngoLogin/', login, name='ngo-login'),
    path('logout/', logout, name='user-logout'),
    path('profile/', profile, name='user-profile'),
    path('hospitalProfile/', hospitalProfile, name='hospital-profile'),
    path('ngoProfile/', ngoProfile, name='ngo-Profile'),
    path('profileEdit/', profileEdit, name='user-profileEdit'),
    path('profilePicEdit/', profilePicEdit, name='user-profilePicEdit'),
    path('aadharPicEdit/', aadharPicEdit, name='user-aadharPicEdit'),
    path('registerChoice/', registerChoice, name='user-registerChoice'),
    path('loginChoice/', loginChoice, name='user-loginChoice'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
