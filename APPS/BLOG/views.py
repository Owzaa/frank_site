from django.shortcuts import render
from . models import Post
from datetime import date



def blog(request):
    post = Post.objects.all()
    current_year = date.today().year
    context = {  
    current_year:'current_year' ,
    post:'post',
    }
    return render(request, 'blog/blog.html', context)

