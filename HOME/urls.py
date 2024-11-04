from django.urls import path
from . views import index, clients, login_user



urlpatterns = [
    path('',clients,name="home"),
    path('', index, name='index'),
    path('login', login_user, name="login")


]
