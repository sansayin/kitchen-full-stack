from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import home

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include("order_service.urls")),
    path("kitchen/", include("kitchen_service.urls")),
]
