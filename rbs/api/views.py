""" 
# View APIs

Similar to Django views, the Django Rest Framework allows urls to be mapped to views that derive from 
the Framework's APIViews providing the various API capabilities the framework provides.
This makes it very easy to provide APIs for the application.

You can view the django-rest-framework documentation [here](http://www.django-rest-framework.org/).
"""
""" 
View API Classes:

1. ***ContactCreateAPIView***: Create a new contact.
2. ***ContactDetailAPIView***: Returns details of a contact.
3. ***ContactListAPIView***: Return a list of all the existing contacts.
4. ***InvoiceCreateAPIView***: Create a new invoice.
5. ***InvoiceDetailAPIView***: Returns details of a invoice.
6. ***InvoiceListAPIView***: Return a list of all the existing invoices.
7. ***AccountCreateAPIView***: Create a new account.
8. ***AccountDetailAPIView***: Returns details of a account.
9. ***AccountListAPIView***: Return a list of all the existing accounts.
10. ***TransactionCreateAPIView***: Create a new transaction.
11. ***TransactionDetailAPIView***: Returns details of a transaction.
12. ***TransactionListAPIView***: Return a list of all the existing transactions.
13. ***ForecastAPIView***: Returns a cashflow forecast plan.
"""

# === Imports ===

# Import django-rest-framework modules
from rest_framework import generics
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# Import Django modules

# Import Bankifi/Cashflow Models

# Import Demo serializers

# Import other models
from nordea.helpers import nordea_api
from nordea.breakdown import get_breakdown

# === Globals ===

# Hard coded receivable account for the demo



# === View Classes


class ForecastAPIView(APIView):
    """
    **ForecastAPIView(APIView)**

    Returns a transaction money in/out overview.

    This API is used by Ajax requests within the Forecast template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        breakdown = get_breakdown()
            
        data = {
            "total_labels": breakdown.get('totalsum').get('months'),
            "total_data": breakdown.get('totalsum').get('totals'),
            "total_back": breakdown.get('totalsum').get('back'),
            "total_border": breakdown.get('totalsum').get('border'),
            "debit_labels": breakdown.get('debitsum').get('months'),
            "debit_data": breakdown.get('debitsum').get('totals'),
            "credit_labels": breakdown.get('creditsum').get('months'),
            "credit_data": breakdown.get('creditsum').get('totals'),
        }
        
        return Response(data)





        
        

