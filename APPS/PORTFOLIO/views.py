from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Project

def portfolio(request):
    projects = Project.objects.all()
    proj_count = projects.count()
    current_year = date.today().year
    context = {
        'proj_count': proj_count,
        'projects':projects,
        'current_year':current_year
    }

    return render(request, 'portfolio/portfolio.html',context)


def project_list(request):
    projects = Project.objects.all()
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
