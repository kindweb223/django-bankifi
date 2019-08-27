""" 
# Project Django Forms

Django forms can map HTML elements to Django model classes and provide data validation and automatic 
HTML widgets to represent model attributes.

The forms are instantiated in the application views and rendered in the project HTML template files. 
"""
"""
**Available Form Classes:**

1. ***AccountModelForm***: Form used to display and validate Account Model instances.
2. ***GroupModelForm***: Form used to display and validate Group Model instances.

"""

# === Imports ===

# Import Django modules
from django import forms
from django.forms import HiddenInput
from django.contrib.admin import widgets
from django.core.validators import MaxValueValidator, MinValueValidator,MinLengthValidator 

# Import Bankifi/Aggregate models
from cashflow.models import Account, Transaction

from .models import (
        # Account,
        Group,
        # Transaction,
        Consent,
    )



# === Form Classes ===


class AccountModelForm(forms.ModelForm):
    """
    **AccountModelForm(forms.ModelForm)**

    Form used to display and validate Account Model instances.
    """
    class Meta:
        model = Account
        fields = [
            'bank',
            'name',
            'sortcode',
            'account_number',
            'currency',
            'sweep_account',
            'sweep_min_balance',
        ]

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        super(AccountModelForm, self).__init__(*args, **kwargs)
        self.fields['sweep_account'].queryset = Account.objects.filter(customer=current_user).order_by('bank', 'name')


class GroupModelForm(forms.ModelForm):
    """
    **GroupModelForm(forms.ModelForm)**

    Form used to display and validate Group Model instances.
    """
    class Meta:
        model = Group
        fields = [
            'title',
            'accounts',
        ]

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        super(GroupModelForm, self).__init__(*args, **kwargs)
        self.fields['accounts'].queryset = Account.objects.filter(customer=current_user, consent__isnull=False).order_by('bank', 'name')


class GroupCreateModelForm(forms.ModelForm):
    """
    **GroupModelForm(forms.ModelForm)**

    Form used to display and validate Group Model instances.
    """
    class Meta:
        model = Group
        fields = [
            'title',
        ]


class ConsentCreateForm(forms.Form):
    """
    **ConsentForm(forms.ModelForm)**

    Form used to display and validate Consent Model instances.
    """
    sortcode = forms.CharField(max_length=11, validators=[MinLengthValidator(6)], 
        label="Sort Code/Swift BIC")
    account_number = forms.CharField(max_length=20, 
        validators=[MinLengthValidator(8)], label="Account Number/IBAN")
    class Meta:
        fields = [
            'sortcode',
            'account_number',
        ]



class TransactionModelForm(forms.ModelForm):
    """
    **TransactionModelForm(forms.ModelForm)**

    Form used to display and validate Transaction Model instances.
    """
    class Meta:
        model = Transaction
        fields = [
            'account',
            'transaction_type',
            'description',
            # 'currency',
            'amount',
        ]

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('user')
        super(TransactionModelForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(customer=current_user).order_by('bank', 'name')


class AuthenticateForm(forms.Form):
    """
    **AuthenticateForm(forms.ModelForm)**

    Form used to display and validate Authenticate Model instances.
    """
    userid = forms.CharField(label="User Id")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    class Meta:
        fields = [
            'userid',
            'password',
        ]
 