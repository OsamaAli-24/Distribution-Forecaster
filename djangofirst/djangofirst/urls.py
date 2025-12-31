from dashboard.views import dashboard_home  # Import the view
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_home, name="dashboard"),  # This makes it the homepage
]
