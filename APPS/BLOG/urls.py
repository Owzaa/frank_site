from django.urls import path
from . import views

urlpatterns = [

    path('', views.blog, name='blog'),
    path('',views.Post_details, name='post-details')

]
