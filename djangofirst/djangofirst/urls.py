from dashboard.views import dashboard_home
from django.contrib import admin
from django.urls import path
# Update imports to include 'delete_product'
from inventory.views import (
    product_list,
    add_stock,
    add_product,
    edit_product,
    delete_product,
    category_list,
    add_category
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_home, name="dashboard"),

    # ==========================
    # PRODUCT URLs
    # ==========================
    path("products/", product_list, name="product_list"),
    path("products/add-stock/", add_stock, name="add_stock"),
    path("products/add/", add_product, name="add_product"),
    path("products/edit/<int:pk>/", edit_product, name="edit_product"),
    path("products/delete/<int:pk>/", delete_product, name="delete_product"), # <--- New Delete Path

    # ==========================
    # CATEGORY URLs
    # ==========================
    path("categories/", category_list, name="category_list"),
    path("categories/add/", add_category, name="add_category"),
]
