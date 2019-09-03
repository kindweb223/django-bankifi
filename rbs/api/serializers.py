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

# Import Bankifi/Cashflow models
from nordea.models import Contact, Account, Transaction



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



class AccountModelSerializer(serializers.ModelSerializer):
    """
    **AccountModelSerializer(serializers.ModelSerializer)**

    Account serializer.
    """
    class Meta:
        model = Account
        fields = [
            'id',
            'bank',
            'name',
            'sortcode',
            'account_number',
        ]


class TransactionModelSerializer(serializers.ModelSerializer):
    """
    **TransactionModelSerializer(serializers.ModelSerializer)**

    Transaction serializer.
    """
    class Meta:
        model = Transaction
        fields = [
            'id',
            'created',
            'account',
            'transaction_type',
            'description',
            'amount',
        ]

        