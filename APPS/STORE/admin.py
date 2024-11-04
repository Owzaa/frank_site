from django.contrib import admin

from . models import Category,Product,Order



# Registered models.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)