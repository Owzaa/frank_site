from django.contrib import admin
from .models import Category, Project, ProjectImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_start', 'project_finished', 'published', 'featured')
    list_filter = ('published', 'featured', 'category')
    search_fields = ('title', 'client', 'technology')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'title')
    search_fields = ('project__title',)
