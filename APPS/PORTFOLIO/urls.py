from django.urls import path
from . import views

urlpatterns = [

    path('portfolio', views.portfolio, name='portfolio'),
    path('projects', views.project_list, name='projeect_list'),
    path('project-details/<int:pk>/',views.project_detail, name="project_detail")
]
