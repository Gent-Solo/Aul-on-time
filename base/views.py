from django.shortcuts import render, get_object_or_404, redirect
from base.models import Meal, Order, OrderItem
from django.views import generic
from django.contrib import messages
from django.utils import timezone


class HomeView(generic.ListView):
    model = Meal
    template_name = 'home.html'


class MealDetailView(generic.DetailView):
    model = Meal
    template_name = 'detail.html'


def add_to_cart(request, pk):
    item = get_object_or_404(Meal, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("core:product", pk=pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("core:product", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("core:product", pk=pk)



