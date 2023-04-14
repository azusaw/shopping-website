from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from shopping.models import Customer


class ShoppingViewsTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        # Create customer user
        self.customer_user = User.objects.create_user(username='test-customer')
        self.customer_user.set_password('Aberdeen2022')
        self.customer_user.save()
        Customer.objects.create(user=self.customer_user, phone="1234567890", address="123 Aberdeen")

        # Create staff user
        self.staff_user = User.objects.create_superuser(username='test-staff')
        self.staff_user.set_password('Aberdeen2022')
        self.staff_user.save()
        Customer.objects.create(user=self.staff_user, phone="0987654321", address="321 Aberdeen")

        self.client = Client()

    def test_view_item_list(self):
        """
        View Test: 1
        Expected: 200 OK
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/item_list.html')
        self.assertContains(response, "All Items")
        self.assertContains(response, "Turtle Check Men Navy Blue Shirt")

    def test_view_use_correct_template_item_list(self):
        """
        View Test: 2
        Expected: 200 OK
        """
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/item_list.html')

    def test_view_item_detail(self):
        """
        View Test: 3
        Expected: 200 OK
        """
        response = self.client.get('/detail/15970')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Turtle Check Men Navy Blue Shirt")

    def test_view_use_correct_template_item_detail(self):
        """
        View Test: 4
        Expected: 200 OK
        """
        response = self.client.get(reverse('item_detail', args=['15970']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/item_detail.html')

    def test_view_signup(self):
        """
        View Test: 5
        Expected: 200 OK
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign Up")

    def test_view_use_correct_template_signup(self):
        """
        View Test: 6
        Expected: 200 OK
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/signup.html')

    def test_view_login(self):
        """
        View Test: 7
        Expected: 200 OK
        """
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_view_use_correct_template_login(self):
        """
        View Test: 8
        Expected: 200 OK
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_view_basket(self):
        """
        View Test: 9
        Expected: 200 OK
        """
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Basket")

    def test_view_use_correct_template_basket(self):
        """
        View Test: 10
        Expected: 200 OK
        """
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/basket.html')

    def test_view_purchase_customer(self):
        """
        View Test: 11
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get('/purchase/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Payment for Your Order")

    def test_view_purchase_staff(self):
        """
        View Test: 12
        Expected: 302 Redirect
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get('/purchase/')
        self.assertEqual(response.status_code, 302)

    def test_view_purchase_without_login(self):
        """
        View Test: 13
        Expected: 302 Redirect
        """
        response = self.client.get('/purchase/')
        self.assertEqual(response.status_code, 302)

    def test_view_use_correct_template_purchase(self):
        """
        View Test: 14
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get(reverse('purchase'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/purchase.html')

    def test_view_order_list_customer(self):
        """
        View Test: 15
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get('/order_list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order History")

    def test_view_order_list_staff(self):
        """
        View Test: 16
        Expected: 200 OK
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get('/order_list/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order History")

    def test_view_order_list_without_login(self):
        """
        View Test: 17
        Expected: 302 Redirect
        """
        response = self.client.get('/order_list/')
        self.assertEqual(response.status_code, 302)

    def test_view_use_correct_template_order_list(self):
        """
        View Test: 18
        Expected: 200 OK
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/order_list.html')

    def test_view_order_customer(self):
        """
        View Test: 19
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get('/order/33/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order Detail")
        self.assertContains(response, "33")

    def test_view_order_staff(self):
        """
        View Test: 20
        Expected: 200 OK
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get('/order/33/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order Detail")
        self.assertContains(response, "33")

    def test_view_order_without_login(self):
        """
        View Test: 21
        Expected: 302 Redirect
        """
        response = self.client.get('/order/33/')
        self.assertEqual(response.status_code, 302)

    def test_view_use_correct_template_order(self):
        """
        View Test: 22
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get(reverse('order_detail', kwargs=dict(order_id=33)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/order_detail.html')

    def test_view_thanks(self):
        """
        View Test: 23
        Expected: 200 OK
        """
        response = self.client.get('/thanks/33')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you for shopping!")
        self.assertContains(response, "33")

    def test_view_use_correct_template_thanks(self):
        """
        View Test: 24
        Expected: 200 OK
        """
        response = self.client.get(reverse('thanks', kwargs=dict(order_id=33)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/order_thanks.html')

    def test_view_profile_customer(self):
        """
        View Test: 25
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")
        self.assertContains(response, "123 Aberdeen")

    def test_view_profile_staff(self):
        """
        View Test: 26
        Expected: 302 Redirect
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_view_profile_without_login(self):
        """
        View Test: 27
        Expected: 302 Redirect
        """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_view_use_correct_template_profile(self):
        """
        View Test: 28
        Expected: 200 OK
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/user_profile.html')

    def test_view_dashboard_staff(self):
        """
        View Test: 29
        Expected: 200 OK
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")

    def test_view_dashboard_customer(self):
        """
        View Test: 30
        Expected: 302 Redirect
        """
        # Login as customer user
        self.client.login(username=self.customer_user.username, password='Aberdeen2022')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_view_dashboard_without_login(self):
        """
        View Test: 31
        Expected: 302 Redirect
        """
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_view_use_correct_template_dashboard(self):
        """
        View Test: 32
        Expected: 200 OK
        """
        # Login as staff user
        self.client.login(username=self.staff_user.username, password='Aberdeen2022')

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
