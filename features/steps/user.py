"""
Behave test
Testing access permission by user type
"""
from behave import *
from django.contrib.auth.models import User

from shopping.models import Customer

use_step_matcher("re")


@given("I am not authenticated")
def guest_user(context):
    pass


@given("I am a customer user")
def customer_user(context):
    # Create test customer user if not exist
    user = User.objects.filter(username="customer-test")
    if not user.exists():
        user = User.objects.create_user("customer-test", "P@ssw0rd")
        Customer.objects.get_or_create(user=user, phone="1234567890", address="123 Aberdeen")
    else:
        user = user.first()
    context.test.client.force_login(user)


@given("I am a staff user")
def staff_user(context):
    # Create test staff user if not exist
    user = User.objects.filter(username="staff-test")
    if not user.exists():
        user = User.objects.create_superuser("staff-test", "P@ssw0rd")
    else:
        user = user.first()
    context.test.client.force_login(user)


@when("I access the item listing page")
def access_item_list_page(context):
    context.response = context.test.client.get("/")


@when("I access the basket page")
def access_basket_page(context):
    context.response = context.test.client.get("/basket/")


@when("I access the purchase page")
def access_purchase_page(context):
    context.response = context.test.client.get("/purchase/")


@when("I access the dashboard page")
def access_dashboard_page(context):
    context.response = context.test.client.get("/dashboard/")


@when("I access the profile page")
def access_profile_page(context):
    context.response = context.test.client.get("/profile/")


@when("I access the order listing page")
def access_order_list_page(context):
    context.response = context.test.client.get("/order_list/")


@then("Status code is (?P<status>\d+)")
def check_status_code(context, status):
    code = context.response.status_code
    assert code == int(status), "{0} != {1}".format(code, status)
