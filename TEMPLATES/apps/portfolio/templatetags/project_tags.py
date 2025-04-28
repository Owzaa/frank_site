from django import template
from APPS.PORTFOLIO.models import Project

register = template.Library()

@register.simple_tag


def get_projects() -> list[Project]:
    return Project.objects.all()
@register.simple_tag
def get_featured_projects():
    return Project.objects.filter(featured=True)

@register.simple_tag 
def get_recent_projects(num=3):
    return Project.objects.order_by('-created_date')[:num]

@register.filter
def truncate_description(value, length=100):
    if len(value) <= length:
        return value
    return value[:length] + '...'
