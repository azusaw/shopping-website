from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from shopping.forms import SignUpForm, PaymentForm, CustomerProfileForm
from shopping.models import Customer, Order, OrderItem
from shopping.views.basket import Basket
from shopping.views.menu import get_menu_info


def signup(request):
    form = SignUpForm(request.POST)
    errors = []

    if request.method == "POST":
        errors = form.errors

    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.customer.phone = form.cleaned_data.get('phone')
        user.customer.address = form.cleaned_data.get('address')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')

    print(form.fields["password1"].help_text)

    return render(request, 'signup.html',
                  {'menu': get_menu_info(), 'form': form, 'password_helper': form.fields["password1"].help_text,
                   'errors': errors})


@login_required
def login(request):
    user = request.user

    if user.is_authenticated:
        return render(request, 'items.html')
    return redirect('login')


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie("sessionid")
    return response


def purchase(request):
    if request.user.is_authenticated:
        user = request.user
        form = PaymentForm(initial={
            'name': f"{user.first_name} {user.last_name}",
        })
        basket = Basket(request)
        return render(request, 'purchase.html',
                      {'menu': get_menu_info(), 'basket': basket, 'user': user, 'form': form})
    return redirect('login')


def payment(request):
    basket = Basket(request)
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.id)
    order = Order.objects.create(customer=customer, total_price=basket.get_total_price())
    order.refresh_from_db()

    for basket_item in basket:
        print(basket_item['item'].item)
        item = basket_item['item'].item
        print(item, basket_item['quantity'])
        order_item = OrderItem.objects.create(order=order, item=item, price=basket_item['price'],
                                              quantity=basket_item['quantity'])
        order_item.refresh_from_db()

    basket.clear()
    request.session['deleted'] = 'thanks for your purchase'
    return redirect("thanks", id=order.id)


def profile(request):
    errors = []

    # Not customer user does not have customer information
    if request.user.is_staff or request.user.is_superuser:
        return redirect('login')

    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        errors = form.errors
    else:
        # Fill fields with a customer information
        form = CustomerProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': customer.phone,
            'address': customer.address,
        })

    if form.is_valid():
        # Update customer information
        customer.phone = request.POST.get("phone")
        customer.address = request.POST.get("address")
        customer.save()
        return redirect('profile')

    return render(request, 'customer_profile.html',
                  {'menu': get_menu_info(), 'form': form, 'errors': errors})
