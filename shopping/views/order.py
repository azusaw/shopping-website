from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from shopping.models import Order, OrderItem, Customer, Image
from shopping.views.menu import get_menu_info


@login_required
def order_list(request):
    # Staff user can see every order
    if request.user.is_staff:
        orders = Order.objects.all().order_by("-created_date")
    else:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.all().filter(customer=customer).order_by("-created_date")
    return render(request, 'order_list.html', {'menu': get_menu_info(), 'orders': orders})


@login_required
def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)

    # Get order items with item instance
    order_items = OrderItem.objects.select_related("item").filter(order_id=id).order_by("item_id")

    # Get images from item ids
    item_ids = [item.item.id for item in order_items]
    images = Image.objects.select_related("item").filter(item__in=item_ids).order_by("item_id")

    # Combine two infomation
    items_with_image = []
    for i in range(0, len(order_items)):
        items_with_image.append({'link': images[i], 'item': order_items[i].item, 'price': order_items[i].price,
                                 'quantity': order_items[i].quantity})

    return render(request, 'order_detail.html',
                  {'menu': get_menu_info(), 'order': order, 'user': user, 'items_with_image': items_with_image})


def thanks(request, id):
    return render(request, 'order_thanks.html', {'menu': get_menu_info(), 'order_id': id})
