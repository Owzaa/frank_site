from django.contrib import admin
from . models import Category,Product,Order,ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'price']


# Registered models.

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ProductImage)
