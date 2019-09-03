""" 
# Rest Framework Serializers

Serializers are like Django forms and allow us to define the fields we want to add to the API JSON.
"""
"""
Serializer Classes:

1. ***ContactModelSerializer***: contact serializer
2. ***InvoiceModelSerializer***: invoice serializer
3. ***AccountModelSerializer***: account serializer
4. ***TransactionModelSerializer***: transaction serializer
"""

# Import django-rest-framework modules
from rest_framework import serializers

from django.contrib.auth.models import User

# Import Bankifi/Cashflow models
from cashflow.models import Contact, Invoice, Account, Transaction



class ContactModelSerializer(serializers.ModelSerializer):
    """
    **ContactModelSerializer(serializers.ModelSerializer)**

    Contact serializer.
    """
    class Meta:
        model = Contact
        fields = [
            'id',
            'name',
            'first_name',
            'last_name',
        ]



class InvoiceModelSerializer(serializers.ModelSerializer):
    """
    **InvoiceModelSerializer(serializers.ModelSerializer)**

    Invoice serializer.
    """
    contact = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'number',
            'invoice_type',
            'contact',
            'raised',
            'due',
            'expected',
            'planned',
            'amount',
            'status',
		]



class AccountModelSerializer(serializers.ModelSerializer):
    """
    **AccountModelSerializer(serializers.ModelSerializer)**

    Account serializer.
    """
    balance = serializers.SerializerMethodField()

    
    class Meta:
        model = Account
        fields = [
            'id',
            'customer',
            'bank',
            'name',
            'sortcode',
            'account_number',
            'currency',
            'balance',
		]

    def get_balance(self, obj):
        user = self.context["user"]
        balance = obj.balance(user)

        return balance



class TransactionModelSerializer(serializers.ModelSerializer):
    """
    **TransactionModelSerializer(serializers.ModelSerializer)**

    Transaction serializer.
    """
    class Meta:
        model = Transaction
        fields = [
            'id',
            'customer',
            'account',
            'transaction_type',
            'description',
            'currency',
            'amount',
		]


		