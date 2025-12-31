from django.contrib import admin

from .models import Category, Product


# This makes the table show columns!
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_quantity", "sku")
    list_filter = ("category",)  # Adds a filter sidebar
    search_fields = ("name", "sku")  # Adds a search bar


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
