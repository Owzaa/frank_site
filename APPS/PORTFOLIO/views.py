# frank_site/APPS/PORTFOLIO/views.py


from django.views.generic import ListView, DetailView
from .models import Project, Tag
from django.shortcuts import get_object_or_404


class PortfolioView(ListView):
    model = Project
    template_name = 'portfolio/portfolio.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(published=True)
        return queryset


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/includes/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(published=True)
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tag'] = self.kwargs.get('tag_slug')
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context['related_projects'] = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id)
        return context
        