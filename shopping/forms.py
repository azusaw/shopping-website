from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """
    Form used for signup user in /signup page
    """
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone = forms.CharField(max_length=13)
    address = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address')


class BasketAddItemForm(forms.Form):
    """
    Form used for updating quantity in /basket page
    """
    # Maximum 30 for each product
    quantity = forms.fields.ChoiceField(
        choices=((x, x) for x in range(1, 31)),
        widget=forms.widgets.Select(attrs={'class': 'form-control quantity'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class PaymentForm(forms.Form):
    """
    Form used for payment in /payment page
    """
    name = forms.CharField(
        label="Name",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    card_number = forms.CharField(
        label="CardNumber",
        max_length=16,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    expire_info = forms.CharField(
        label="Expire Info",
        max_length=5,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/yy'})
    )
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CustomerProfileForm(forms.Form):
    """
    Form used for updating customer information in /profile page
    """
    first_name = forms.CharField(
        label="First Name",
        disabled=True,
        required=False,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Last Name",
        disabled=True,
        required=False,
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label="Phone Number",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Address",
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )
