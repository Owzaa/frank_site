from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('category/<slug>/', views.category, name='category'),
    path('post/<slug>/', views.post_detail, name='post_detail'),
]

