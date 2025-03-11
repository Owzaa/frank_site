from django.shortcuts import render,get_object_or_404
from datetime import date
from APPS.STORE.models import Product
from . models import Client, Interest
from APPS.BLOG.models import Post


def index(request):
    posts= Post.objects.all() 
    client = Client.objects.all() 
    current_year = date.today().year
    context =  {   
    'posts': posts,  
    'client':client,   
    'current_year': current_year,
    }

    return render(request, 'home/home.html', context )
    
def clients(request):
    client = Client.objects.all() 
  
    return render(request,"home/home.html",{'client':client})

def home(request,pk):
    posts = Post.objects.all()
    post_detail = get_object_or_404(Post,pk=pk)
    current_year = date.today().year
    context =  {
    'current_year':current_year,
    'post_detail':post_detail,
    'posts':posts,   
    }

    return render(request,'home/home.html', context )
    
    

    
    
def login_user(request):
    current_year = date.today().year

    return render(request,"login/login.html",{'current_year':current_year})

def blog(request):
    posts = Post.objects.all()
    current_year = date.today().year
    context = {
    'current_year': current_year,
    'posts': posts,
    }
    return render(request, 'blog/blog.html', context)

def Post_details(request,pk):
    posts = get_object_or_404(Post,pk=pk)
    current_year = date.today().year

    context = {
    'current_year': current_year,
    'posts': posts,
    'post_detail':post_detail,
    }
    return render(request, 'blog/post_detail.html', context)


def shop (request):
    current_year = date.today().year
    return render(request, 'home/home.html', {'current_year':current_year})


    
def interest(request):
    interest = Interest.objects.all()
    title = "Interests"
  
    return render(request,"home/home.html",{'interest':interest})

def product(request):
    product = Product.objects.all()
    return render(request,'products/product_slider.html',
                        {'product':product })
