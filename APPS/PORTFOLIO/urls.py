from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('category/<slug:category_slug>/', views.portfolio_category, name='portfolio_categories'),
    path('category/<slug:category_slug>/<slug:item_slug>/', views.portfolio_detail, name='portfolio_detail'),
]
