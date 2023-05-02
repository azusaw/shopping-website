from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from shopping.models import Order, OrderItem, Customer
from shopping.views.menu import get_menu_info


@login_required
def order_list(request):
    """
    Render '/order_list' page with order data
    """
    # Staff user can see every order
    if request.user.is_staff:
        orders = Order.objects.all().order_by("-created_date")
    else:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.all().filter(customer=customer).order_by("-created_date")
    return render(request, 'pages/order_list.html', {'menu': get_menu_info(), 'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Render '/order/<order_id>' page with selected order data
    """
    order = get_object_or_404(Order, id=order_id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)

    # Get order items with item instance
    order_items = OrderItem.objects.select_related("item").filter(order_id=order_id).order_by("item_id")

    return render(request, 'pages/order_detail.html',
                  {'menu': get_menu_info(), 'order': order, 'user': user, 'order_items': order_items})


def thanks(request, order_id):
    """
    Render '/thanks/<order_id>' page
    """
    return render(request, 'pages/order_thanks.html', {'menu': get_menu_info(), 'order_id': order_id})
