from django.urls import path
from .views import index,clients,interest,blog,login_user
from . import  views   


urlpatterns = [    
    path('', views.index, name='index'),  
    path('', clients, name='clients'), 
    path('login/', login_user, name="login"),    
    path('blog/', blog,name="blog"),

]
