from django.urls import path
from . views import shop, product

urlpatterns = [

    path('shop/', shop, name='shop'),
    path('product/', product, name="product")





]
