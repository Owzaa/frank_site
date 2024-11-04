
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
