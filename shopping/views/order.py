from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from shopping.models import Order, OrderItem, Customer
from shopping.views.menu import get_menu_info


def order_list(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.all().filter(customer=customer)
    return render(request, 'order_list.html', {'menu': get_menu_info(), 'orders': orders})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    customer = order.customer
    user = get_object_or_404(User, id=customer.pk)
    order_items = OrderItem.objects.select_related("item").filter(order_id=id)
    return render(request, 'order_detail.html',
                  {'menu': get_menu_info(), 'order': order, 'user': user, 'order_items': order_items})
