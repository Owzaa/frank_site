from django.contrib import admin

from . models import PortfolioCategory, PortfolioItem, Project,   ProjectImage

class PortfolioItemInline(admin.TabularInline):
    model = PortfolioItem
    extra = 1

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'item_count')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PortfolioItemInline]

    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Items"

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client', 'project_date', 'featured', 'published')
    list_filter = ('category', 'featured', 'published')
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'project_date'


class ProjectImageInline(admin.TabularInline):
    model= ProjectImage
    extra = 1


@admin.register(Project)

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]

admin.site.register(ProjectImage)

