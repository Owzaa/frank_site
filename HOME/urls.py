from django.urls import path
from . views import index, clients, login_user,blog



urlpatterns = [
    path('',clients,name="home"),
    path('', index, name='index'),
    path('login', login_user, name="login"),
    path('blog', blog, name="blog")


]
