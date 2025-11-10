# orders/forms.py
from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150, required=True)
    phone = forms.CharField(max_length=30, required=True)
    address_line1 = forms.CharField(max_length=255, required=True, label="Address line 1")
    address_line2 = forms.CharField(max_length=255, required=False, label="Address line 2")
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    postal_code = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=100, required=True)
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('CARD', 'Card (Fake)'),
    )
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect, initial='COD')
