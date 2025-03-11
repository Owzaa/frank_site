from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category
from django.db.models  import Count, Q
from datetime import date

def blog(request):
    # Search functionality
    search_query = request.GET.get('q', '')
    current_year = date.today().year    
    # Get published posts with search filter
    posts_list = Post.objects.filter(
        Q(title__icontains=search_query) | 
        Q(content__icontains=search_query),
        status='published'
    ).order_by('-published_at')

    # Pagination (6 posts per page)
    page = request.GET.get('page')
    paginator = Paginator(posts_list, 6 )
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Get categories with post counts
    categories = Category.objects.annotate(
    post_count = Count('posts', filter=Q(posts__status='published'))
    )

    context = {'current_year':current_year,
        'posts': posts,
        'categories': categories,
        'search_query': search_query
    }
    return render(request, 'blog/blog.html', context)
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    search_query = request.GET.get('q', '')
    
    posts_list = Post.objects.filter(
        Q(title__icontains=search_query) |
        Q(content__icontains=search_query),
        category=category,
        status='published'
    ).order_by('-published_at')

    paginator = Paginator(posts_list, 9)  # 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages()
    }
    return render(request, 'blog/category.html', context)

def post_detail(request, slug):
    """
    View for a specific post.

    Handles related posts.
    """
    post = get_object_or_404(Post, slug=slug, status='published')
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'related_posts': related_posts
    }
    return render(request, 'blog/post_detail.html', context)