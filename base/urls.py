from django.urls import path
from base.views import list_food_item

urlpatterns = [
    path("food-list/", list_food_item)
]
