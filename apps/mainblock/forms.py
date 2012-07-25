# -*- coding: utf-8 -*-
from django import forms
from apps.mainblock.models import Order

class OrderForm(forms.ModelForm):
    fullname = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )
    contacts = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )
    note = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )

    class Meta:
        model = Order
        exclude = ('create_date')