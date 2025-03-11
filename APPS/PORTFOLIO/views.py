from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import PortfolioCategory, PortfolioItem, Project

def portfolio(request):
    projects = PortfolioItem.objects.all()
    proj_count = projects.count()
    current_year = date.today().year
    context = {
    'proj_count': proj_count,
    'projects':projects,
    'current_year':current_year,
    }

    return render(request, 'portfolio/portfolio.html',context)


def project_list(request):
    projects = PortfolioItem.objects.all()
    proj_count = projects.count()
    context = {
        'projects':projects,
        'proj_count': proj_count,
    }
    return render(request, 'portfolio/portfolio.html',context)


def project_detail(request,pk):
    project = get_object_or_404(Project, pk=pk)
    current_year = date.today().year
    context = {
    'project':project,
    'current_year':current_year
    }
    return render(request,'portfolio/project_detail.html',context)


def portfolio_categories(request):
    categories = PortfolioCategory.objects.filter(
        items__published=True
    ).distinct().order_by('order')

    context = {
        'categories': categories
    }
    return render(request, 'portfolio/categories.html', context)

def portfolio_category(request,category_slug):
    category = get_object_or_404(PortfolioCategory, slug=category_slug)
    items = category.items.filter(published=True).order_by('-project_date')

    context = {
        'category': category,
        'items': items
    }
    return render(request, 'portfolio/category_items.html', context)

def portfolio_detail(request, category_slug, item_slug):
    item = get_object_or_404(PortfolioItem,
                            slug=item_slug,
                            category__slug=category_slug,
                            published=True)

    context = {
        'item': item,
        'related_items': PortfolioItem.objects.filter(
            category=item.category,
            published=True
        ).exclude(id=item.id)[:4]
    }
    return render(request, 'portfolio/detail.html', context)
