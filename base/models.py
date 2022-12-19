from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    phone = models.TextField(blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Meal(models.Model):
    CAFE = (
        ("cafe 1", "Café 1"),
        ("cafe 2", "Cafe 2"),
    )
    cafe = models.CharField(max_length=10, choices=CAFE, default="Cafe 1")
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=100)
    image = models.ImageField(upload_to="", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    discount_price = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk": self.pk

        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            "pk": self.pk
        })

    def __str__(self):
        return f"{self.name} {self.cafe}"


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.meal.name}"

    def get_total_item_price(self):
        return self.quantity * self.meal.price

    def get_discount_item_price(self):
        return self.quantity * self.meal.discount_price

    def get_final_price(self):
        if self.meal.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
