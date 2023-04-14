from django.test import TestCase
from django.utils import timezone

from shopping.forms import SignUpForm, BasketAddItemForm, PaymentForm


class FormTest(TestCase):
    fixtures = ['test_data.json']

    def test_form_signup_valid(self):
        """ Form Test: 1 """
        data = {
            'username': 'test-user1',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())
        customer = form.save(commit=False)
        customer.created_date = timezone.now()
        customer.save()
        self.assertEqual(customer.username, 'test-user1')

    def test_form_signup_invalid_username(self):
        """ Form Test: 2 """
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_username_length(self):
        """ Form Test: 3 """
        data = {
            'username': 'OVER30OVER30OVER30OVER30OVER30!',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_first_name(self):
        """ Form Test: 4 """
        data = {
            'username': 'test-user-invalid',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_first_name_length(self):
        """ Form Test: 5 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'OVER30OVER30OVER30OVER30OVER30!',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_last_name(self):
        """ Form Test: 6 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_last_name_length(self):
        """ Form Test: 7 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'OVER30OVER30OVER30OVER30OVER30!',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_without_password1(self):
        """ Form Test: 8 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_without_password2(self):
        """ Form Test: 9 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_password_weak(self):
        """ Form Test: 10 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "password",
            'password2': "password",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_password_confirmation(self):
        """ Form Test: 11 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr9",
            'phone': '01234567',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_whithout_phone(self):
        """ Form Test: 12 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_phone_length(self):
        """ Form Test: 13 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '12345678901234',
            'address': '123 Aberdeen'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_without_address(self):
        """ Form Test: 14 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_signup_invalid_address_length(self):
        """ Form Test: 15 """
        data = {
            'username': 'test-user-invalid',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': "Kwani87gr98",
            'password2': "Kwani87gr98",
            'phone': '01234567',
            'address': 'OVER50OVER50OVER50OVER50OVER50OVER50OVER50OVER50OVER50'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_basket_add_valid(self):
        """ Form Test: 16 """
        data = {
            'quantity': 3,
        }
        form = BasketAddItemForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_basket_add_without_quantity(self):
        """ Form Test: 17 """
        data = {}
        form = BasketAddItemForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_payment_valid(self):
        """ Form Test: 18 """
        data = {
            'name': "TEST USER",
            'card_number': "1234567890123456",
            "expire_info": "12/26"
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_payment_without_name(self):
        """ Form Test: 19 """
        data = {
            'card_number': "1234567890123456",
            "expire_info": "12/26"
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_payment_without_card_number(self):
        """ Form Test: 20 """
        data = {
            'name': "TEST USER",
            "expire_info": "12/26"
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_payment_invalid_card_number_length(self):
        """ Form Test: 21 """
        data = {
            'name': "TEST USER",
            'card_number': "12345678901234567",
            "expire_info": "12/26"
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_payment_without_expire_info(self):
        """ Form Test: 22 """
        data = {
            'name': "TEST USER",
            'card_number': "1234567890123456",
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid() is False)

    def test_form_payment_invalid_expire_info_length(self):
        """ Form Test: 23 """
        data = {
            'name': "TEST USER",
            'card_number': "1234567890",
            "expire_info": "12/260"
        }
        form = PaymentForm(data=data)
        self.assertTrue(form.is_valid() is False)
