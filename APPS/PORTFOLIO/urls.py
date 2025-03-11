from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.portfolio_categories, name='portfolio'),
    path('project-detail/<pk>', views.project_detail, name='project_detail'),
    path('portfolio-categories/', views.portfolio_categories, name='portfolio_categories'),
    path('portfolio/<slug:category_slug>/', views.portfolio_category, name='portfolio_category'),
    path('portfolio/<slug:category_slug>/<slug:item_slug>/', views.portfolio_detail, name='portfolio_detail'),
]
