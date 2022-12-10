from django.shortcuts import render
from base.models import Food

def list_food_item(request):
    foods = Food.objects.all()
    print(foods)
    context = {
        'foods':foods
    }
    return render(request, "index.html", context)