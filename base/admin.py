from django.contrib import admin
from .models import Meal, OrderItem, Order

admin.site.register(Meal)
admin.site.register(OrderItem)
admin.site.register(Order)
