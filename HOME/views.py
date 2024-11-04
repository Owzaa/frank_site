from django.shortcuts import render
from datetime import date
from APPS.STORE.models import Product
from .models import Client

def index(request):
    current_year = date.today().year
    return render(request, 'home/home.html', {'current_year':current_year})


def login_user(request):
    current_year = date.today().year

    return render(request,"login/login.html",{'current_year':current_year})



def shop (request):
    current_year = date.today().year
    return render(request, 'home/home.html', {'current_year':current_year})





def clients(request):
    client = Client.objects.all()
    title = "Happy-Client"


    return render(request,"home/home.html",{'client':client})


def product(request):
    product = Product.objects.all()
    return render(request,'products/product_slider.html',
                        {'product':product })
