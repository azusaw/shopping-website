from django.contrib.auth.decorators import login_required
from django.db import models
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
        user.save()

        customer = Customer(user=user, phone=form.cleaned_data.get('phone'), address=form.cleaned_data.get('address'))
        customer.save()
        return redirect('/accounts/login/')

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
    return redirect("thanks", order_id=order.id)


def profile(request):
    """
    Render '/profile' page with login user data
    """
    errors = []
    swal_icon = ''
    swal_title = ''
    swal_message = ''

    # Only customer user can access to the profile page
    if not request.user.is_authenticated or request.user.is_staff or request.user.is_superuser:
        return redirect('login')

    customer = Customer.objects.get(user=request.user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.errors:
            errors = form.errors
            swal_icon = "error"
            swal_title = "Error..."
            swal_message = "Failed to update your profile"
        else:
            swal_icon = "success"
            swal_title = "Success!"
            swal_message = "Your profile is updated."

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

    return render(request, 'pages/user_profile.html',
                  {'menu': get_menu_info(), 'form': form, 'errors': errors, 'swal_icon': swal_icon,
                   'swal_title': swal_title, 'swal_message': swal_message})


def dashboard(request):
    """
    Render '/dashboard' page with orders data
    """
    background_colours = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(201, 203, 207, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)'
    ]
    border_colours = [
        'rgb(255, 99, 132)',
        'rgb(255, 159, 64)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(54, 162, 235)',
        'rgb(153, 102, 255)',
        'rgb(201, 203, 207)',
        'rgb(255, 99, 132)',
        'rgb(255, 159, 64)',
        'rgb(255, 205, 86)',
    ]
    chart_colours = {
        'background': background_colours * 4,
        'border': border_colours * 4,
    }

    if request.user.is_staff or request.user.is_superuser:
        # Count order group by month (Recent 4 months)
        order_count = Order.objects.annotate(
            month=TruncMonth('created_date')).values(
            'month').annotate(
            count=Count('id')).values('month', 'count').order_by('-month')[:4]

        # Total sales group by month (Recent 5 months)
        order_sales = Order.objects.annotate(
            month=TruncMonth('created_date')).values(
            'month').annotate(
            sales=models.Sum('total_price')).values('month', 'sales').order_by('-month')[:4]

        # Count order group by gender
        gender_count = OrderItem.objects.select_related("item").values('item__gender').annotate(
            count=Count('id')).values('item__gender', 'count')

        # Count order group by master category
        master_category_count = OrderItem.objects.select_related("item").values('item__master_category').annotate(
            count=Count('id')).values('item__master_category', 'count')

        # Count order group by sub category
        sub_category_count = OrderItem.objects.select_related("item").values('item__sub_category').annotate(
            count=Count('id')).values('item__sub_category', 'count')

        # Count order group by article type
        article_type_count = OrderItem.objects.select_related("item").values('item__article_type').annotate(
            count=Count('id')).values('item__article_type', 'count')

        # Count order group by base colour
        base_colour_count = OrderItem.objects.select_related("item").values('item__base_colour').annotate(
            count=Count('id')).values('item__base_colour', 'item__base_colour__hex_code', 'count')

    else:
        return redirect('login')

    return render(request, 'pages/dashboard.html',
                  {'menu': get_menu_info(),
                   'chart_colours': chart_colours,
                   'order_count': {'label': [f"{row['month'].month}/{row['month'].year}" for row in order_count],
                                   'data': [row["count"] for row in order_count]},
                   'order_sales': {'label': [f"{row['month'].month}/{row['month'].year}" for row in order_sales],
                                   'data': [round(row["sales"], 2) for row in order_sales]},
                   'gender_count': {
                       'label': [row["item__gender"] for row in gender_count],
                       'data': [row["count"] for row in gender_count]},
                   'master_category_count': {
                       'label': [row["item__master_category"] for row in master_category_count],
                       'data': [row["count"] for row in master_category_count]},
                   'sub_category_count': {
                       'label': [row["item__sub_category"] for row in sub_category_count],
                       'data': [row["count"] for row in sub_category_count]},
                   'article_type_count': {
                       'label': [row["item__article_type"] for row in article_type_count],
                       'data': [row["count"] for row in article_type_count]},
                   'base_colour_count': {
                       'label': [row["item__base_colour"] for row in base_colour_count],
                       'colour': [row["item__base_colour__hex_code"] for row in base_colour_count],
                       'data': [row["count"] for row in base_colour_count]},
                   })
