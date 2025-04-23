from django.db import models
from django.utils.text import slugify

# -----------------------------
# Category for Portfolio
# -----------------------------
class Category(models.Model):
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

# -----------------------------
# Main Project (like a portfolio entry)
# -----------------------------
class Project(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    client = models.CharField(max_length=200, blank=True)
    project_start = models.DateField()
    project_finished = models.DateField()
    project_date = models.DateField(help_text="Date of project delivery", blank=True, null=True)
    description = models.TextField()
    content = models.TextField(help_text="Detailed HTML content", blank=True)
    technology = models.CharField(max_length=100, help_text="Main technologies used")
    project_url = models.URLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='portfolio/projects/', null=True, blank=True)
    logo = models.ImageField(upload_to='portfolio/projects/logos/', null=True, blank=True)
    published = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-project_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# -----------------------------
# Extra Images for Project (Gallery/Slider)
# -----------------------------
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='portfolio/projects/gallery/')
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title or 'Image'}"
