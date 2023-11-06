from django.contrib import admin
from order_service.models import Menu, MenuCategory, Order, Payment

admin.site.register([Menu, MenuCategory, Order, Payment])
