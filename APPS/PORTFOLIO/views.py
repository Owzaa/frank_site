# frank_site/APPS/PORTFOLIO/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Project, Category

def portfolio(request):
    # All Projects
    projects = Project.objects.all()
    categories = Category.objects.all()

    # Paginate projects (6 per page)
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX (pagination click)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('portfolio/includes/project_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})

    # Normal full page load
    return render(request, 'portfolio/portfolio.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': None,
    })

def portfolio_category(request, category_slug):
    # Get the category object
    category = get_object_or_404(Category, slug=category_slug)

    # Filter projects belonging to that category
    projects = Project.objects.filter(category=category)

    categories = Category.objects.all()

    # Paginate filtered projects (6 per page)
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX (pagination/filter click)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('portfolio/includes/project_list.html', {'page_obj': page_obj})
        return JsonResponse({'html': html})

    # Normal full page load
    return render(request, 'portfolio/portfolio.html', {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
    })


def portfolio_detail(request, category_slug, item_slug):
    category = get_object_or_404(Category, slug=category_slug)
    project = get_object_or_404(Project, slug=item_slug, category=category)

    return render(request, 'portfolio/portfolio_detail.html', {
        'project': project,
        'category': category,
    })