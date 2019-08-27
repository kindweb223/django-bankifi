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
from django.db.models import Q

# Import Bankifi/Cashflow Models
from nordea.models import (
        Contact, 
        Account, 
        Transaction,
    )

# Import Demo serializers
from .serializers import (
        ContactModelSerializer, 
        AccountModelSerializer,
        TransactionModelSerializer,
    )

# Import other models
from nordea.helpers import nordea_api
from nordea.breakdown import get_breakdown
from nordea.currency import total_networth, total_credits, total_debits
# === Globals ===

# Hard coded receivable account for the demo
RECEIVABLE_ACCOUNT = '51387801-7668-48b0-a276-e8cadc2d33de' 


# === View Classes

class AccountViewSet(viewsets.ModelViewSet):
    """
    View and Edit accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountModelSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]




class ContactViewSet(viewsets.ModelViewSet):
    """
    View and Edit Contacts.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]



class TransactionViewSet(viewsets.ModelViewSet):
    """
    View and Edit Transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]


# === View Classes ===

class ContactCreateAPIView(generics.CreateAPIView):
    """
    **ContactCreateAPIView(generics.CreateAPIView)**

    Create a new contact.
    """
    serializer_class = ContactModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()



class ContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    **ContactDetailAPIView(generics.RetrieveUpdateDestroyAPIView)**

    Returns details of a contact.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactModelSerializer
    permission_classes = [permissions.IsAuthenticated]



class ContactListAPIView(generics.ListAPIView):
    """
    **ContactListAPIView(generics.ListAPIView)**

    Return a list of all the existing contacts.
    """
    serializer_class = ContactModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Contact.objects.all()

        return qs



class NetworthAPIView(APIView):
    """
    **NetworthAPIView(APIView)**

    Returns a Account total balance in different currencies.

    This API is used by Ajax requests within the Aggregate template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols = {'USD': '$', 'GBP': '£', 'EUR': '€'}
        base = request.GET.get('base', 'EUR').upper()
        total = total_networth(base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)



class CreditsAPIView(APIView):
    """
    **CreditsAPIView(APIView)**

    Returns a Account total balance in different currencies.

    This API is used by Ajax requests within the Aggregate template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols = {'USD': '$', 'GBP': '£', 'EUR': '€'}
        base = request.GET.get('base', 'EUR').upper()
        total = total_credits(base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)



class DebitsAPIView(APIView):
    """
    **DebitsAPIView(APIView)**

    Returns a Account total balance in different currencies.

    This API is used by Ajax requests within the Aggregate template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols = {'USD': '$', 'GBP': '£', 'EUR': '€'}
        base = request.GET.get('base', 'EUR').upper()
        total = total_debits(base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)


# class InvoiceCreateAPIView(generics.CreateAPIView):
#     """
#     **InvoiceCreateAPIView(generics.CreateAPIView)**

#     Create a new invoice.
#     """
#     serializer_class = InvoiceModelSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save()



# class InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     **InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView)**
    
#     Returns details of an invoice.
#     """
#     queryset = Invoice.objects.all()
#     serializer_class = InvoiceModelSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class InvoiceListAPIView(generics.ListAPIView):
#     """
#     **InvoiceListAPIView(generics.ListAPIView)**

#     Returns a list of all invoices.
#     """
#     serializer_class = InvoiceModelSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         qs = Invoice.objects.all()
            
#         return qs



class AccountCreateAPIView(generics.CreateAPIView):
    """
    **AccountCreateAPIView(generics.CreateAPIView)**

    Creates a new bank account.
    """
    serializer_class = AccountModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()



class AccountDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    **AccountDetailAPIView(generics.RetrieveUpdateDestroyAPIView)**

    Returns the details of a bank account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountModelSerializer
    permission_classes = [permissions.IsAuthenticated]



class AccountListAPIView(generics.ListAPIView):
    """
    **AccountListAPIView(generics.ListAPIView)**

    Returns a list of bank accounts.
    """
    serializer_class = AccountModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Account.objects.all()
            
        return qs



class TransactionCreateAPIView(generics.CreateAPIView):
    """
    **TransactionCreateAPIView(generics.CreateAPIView)**

    Create a bank account transaction.
    """
    serializer_class = TransactionModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()



class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    **TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView)**

    Returns the details of a bank transaction.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionModelSerializer
    permission_classes = [permissions.IsAuthenticated]



class TransactionListAPIView(generics.ListAPIView):
    """
    **TransactionListAPIView(generics.ListAPIView)**

    Returns a list of bank transactions.
    """
    serializer_class = TransactionModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Transaction.objects.all()
            
        return qs


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





        
        

# class ForecastAPIView(APIView):
#     """
#     **ForecastAPIView(APIView)**

#     Returns a cashflow forecast plan.

#     This API is used by Ajax requests within the Forecast template.
#     """
#     authenticated_classes = []
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         acc = Account.objects.get(account_id=RECEIVABLE_ACCOUNT)
#         pay = Invoice.invoice_obj.pay_monthly()
#         rec = Invoice.invoice_obj.rec_monthly()

#         months = []
#         balance = []
#         back = []
#         border = []
#         acc_bal = acc.balance
#         for m, p, r in zip(pay['months'], pay['totals'], rec['totals']):
#             acc_bal += r - p 
#             balance.append(acc_bal)
#             months.append(m)
#             back.append('rgba(1, 1, 1, 0.2)' if acc_bal >= 0 else 'rgba(255,99,132,0.2)',)
#             border.append('rgba(1, 1, 1, 1)' if acc_bal >= 0 else 'rgba(255,99,132,1)',)
            
        
#         data = {
#             "bal_labels": months,
#             "bal_data": balance,
#             "bal_back": back,
#             "bal_border": border,
#             "pay_labels": pay['months'],
#             "pay_data": pay['totals'],
#             "rec_labels": rec['months'],
#             "rec_data": rec['totals'],
#         }
#         return Response(data)

