from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404

from shopping.forms import SignUpForm, PaymentForm, CustomerProfileForm
from shopping.models import Customer, Order, OrderItem
from shopping.views.basket import Basket
from shopping.views.menu import get_menu_info


def signup(request):
    """
    Render '/signup' page and create new customer user
    """
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

    return render(request, 'pages/signup.html',
                  {'menu': get_menu_info(), 'form': form, 'password_helper': form.fields["password1"].help_text,
                   'errors': errors})


@login_required
def login(request):
    """
    Login with django auth
    """
    user = request.user

    if user.is_authenticated:
        redirect('/')
    return redirect('login')


def logout(request):
    """
    Delete session id cookie to logout
    """
    response = HttpResponseRedirect('/')
    response.delete_cookie("sessionid")
    return response


def purchase(request):
    """
    Render '/purchase' page with basket data
    """
    # Only customer user can process purchase
    if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
        return redirect('login')

    user = request.user
    form = PaymentForm(initial={
        'name': f"{user.first_name} {user.last_name}",
    })
    basket = Basket(request)
    return render(request, 'pages/purchase.html',
                  {'menu': get_menu_info(), 'basket': basket, 'user': user, 'form': form})


def payment(request):
    """
    Process payment and redirect to '/thanks' page
    """
    # Only customer user can process payment
    if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
        return redirect('login')

    basket = Basket(request)
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.id)
    order = Order.objects.create(customer=customer, total_price=basket.get_total_price())
    order.refresh_from_db()

    for basket_item in basket:
        item = basket_item['item'].item
        order_item = OrderItem.objects.create(order=order, item=item, price=basket_item['price'],
                                              quantity=basket_item['quantity'])
        order_item.refresh_from_db()

    basket.clear()
    request.session['deleted'] = 'thanks for your purchase'
    return redirect("thanks", id=order.id)


def profile(request):
    """
    Render '/profile' page with login user data
    """
    errors = []

    # Only customer user can access to the profile page
    if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
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

    return render(request, 'pages/user_profile.html',
                  {'menu': get_menu_info(), 'form': form, 'errors': errors})
