from django.contrib import admin

# Register your models here.

from .models import Category, Product

admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_featured", "is_available")
    list_filter = ("category", "is_featured", "is_available")