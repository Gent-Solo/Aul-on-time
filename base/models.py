from email.policy import default
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Food(models.Model):
    food_name = models.CharField(max_length = 30)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    discount = models.IntegerField()
    available = models.BooleanField(default=True)
    quantity_available = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.food_name} - N{self.price}"
