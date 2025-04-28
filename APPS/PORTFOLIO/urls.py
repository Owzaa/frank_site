from django.urls import path # from django.views.generic import ListView
from . import views


urlpatterns = [
    path('portfolio/', views.PortfolioView.as_view(), name='portfolio'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('tag/<slug:tag_slug>/', views.ProjectListView.as_view(), name='project_list_by_tag'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]