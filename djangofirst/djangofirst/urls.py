from django.contrib import admin
from django.urls import path
from home.views import index  # <--- Import your view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'), # <--- Add this line! (Empty '' means homepage)
]