
from django.db import models


class Project(models.Model):
    project_title = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_start = models.DateField()
    project_finished = models.DateField()
    description = models.TextField()
    technology = models.CharField(max_length=50)
    project_url = models.URLField(name="project_url")
    project_logo = models.ImageField(name="project_logo",upload_to="media/projects")

    def __str__(self):
        return self.project_title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project,related_name='images',on_delete=models.CASCADE)
    slider_title = models.CharField(max_length=100,blank=True)
    image = models.ImageField(upload_to="media/projects/slider_images")
    caption = models.TextField(blank=True)

    def __self__(self):
        return f"{self.project.project_title} - Image"


class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='portfolio/categories/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Portfolio Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(PortfolioCategory, 
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='items')
    client = models.CharField(max_length=200, blank=True)
    project_date = models.DateField()
    description = models.TextField()
    featured_image = models.ImageField(upload_to='portfolio/items/')
    content = models.TextField(help_text="HTML/content for detailed view")
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-project_date']
        
    def __str__(self):
        return self.title