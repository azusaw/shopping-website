import random

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from shopping.models import Customer, Order, Item, OrderItem


def get_random_item(items):
    """Return random item"""
    return items[random.randrange(0, len(items) - 1, 1)]


def get_random_price():
    """Return random price"""
    return round(random.randrange(500, 10000, 1) / 100, 2)


def get_random_date():
    """Returns random dates from this month up to 4 months ago"""
    return timezone.now() + relativedelta(months=-random.randrange(0, 4, 1))


class Command(BaseCommand):
    help = 'Create dummy data'

    def handle(self, *args, **options):
        # Delete data from tables to avoid duplicate values
        print("START: DELETE ALL RECORDS FROM ORDER, ORDER_ITEM, USER, CUSTOMER ")
        Order.objects.all().delete()
        OrderItem.objects.all().delete()
        User.objects.all().delete()
        Customer.objects.all().delete()
        print("--> Delete all record successfully.")

        print("START: CREATE DUMMY DATA")
        fake = Faker()

        # Create admin user data
        superuser = User.objects.create_superuser(
            username='admin',
            first_name='Azusa',
            last_name='Watanabe',
            email='aadmin@email.com',
            password='P@ssw0rd')
        superuser.save()

        # Create customer user data
        user = User.objects.create_user(
            username='azusaw',
            first_name='Azusa',
            last_name='Watanabe',
            email='azusa@email.com',
            password='P@ssw0rd')
        user.save()
        customer = Customer.objects.create(user=user, phone='012345678', address='123 Aberdeen')
        customer.save()

        # Create 10 customer user data
        for i in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            phone = fake.phone_number()
            address = fake.address()
            user = User.objects.create_user(
                username=first_name + last_name,
                first_name=first_name,
                last_name=last_name,
                email=fake.ascii_free_email(),
                password='p@ssw0rd')
            user.save()

            customer = Customer.objects.create(user=user, phone=str(phone[0]), address=str(address[0]))
            customer.save()

        # Create order data
        customers = Customer.objects.all()
        items = Item.objects.all()
        for customer in customers:
            for i in range(3):
                # Each order has two items
                order_items = [get_random_item(items) for x in range(2)]
                total_price = round(order_items[0].price + order_items[1].price, 2)
                order = Order.objects.create(customer=customer, total_price=total_price)

                order.created_date = get_random_date()
                order.save()

                for item in order_items:
                    order_item = OrderItem.objects.create(order=order, item=item, price=item.price, quantity=1)
                    order_item.save()

        print("--> Complete create dummy data successfully.")
