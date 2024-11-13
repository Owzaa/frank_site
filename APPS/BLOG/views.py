from django.shortcuts import render, get_object_or_404
from .models import Post
from datetime import date

def blog(request):
    posts = Post.objects.all()
    current_year = date.today().year
    title = 'Blog'
    context = {
    posts:'posts',
    title:'title',
    current_year:'current_year' ,

    }
    return render(request, 'blog/blog.html', context)

def Post_details(request,pk):
    post = get_object_or_404(Post,pk=pk)
    context = {
    current_year:'current_year',
    post:'post'
    }
    return render(request, 'blog/post-detail.html', context)
