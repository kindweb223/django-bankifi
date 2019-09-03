# === Imports ===

# Import django-rest-framework modules
from rest_framework import generics
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

# Import Django modules

from cashflow.models import Transaction
from aggregate.currency import total_group_balance, total_account_balance, total_networth, total_credits, total_debits

class GroupTotalAPIView(APIView):
    """
    **GroupTotalAPIView(APIView)**

    Returns a Group account total balance in different currencies.

    This API is used by Ajax requests within the Aggregate template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols = {'USD': '$', 'GBP': '£', 'EUR': '€'}
        base = request.GET.get('base', 'EUR').upper()
        total = total_group_balance(self.request.user, base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)


class AccountTotalAPIView(APIView):
    """
    **AccountTotalAPIView(APIView)**

    Returns a Account total balance in different currencies.

    This API is used by Ajax requests within the Aggregate template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        symbols = {'USD': '$', 'GBP': '£', 'EUR': '€'}
        base = request.GET.get('base', 'EUR').upper()
        total = total_account_balance(self.request.user, base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)


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
        total = total_networth(self.request.user, base)
            
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
        total = total_credits(self.request.user, base)
            
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
        total = total_debits(self.request.user, base)
            
        data = {
            "total": total,
            # "total_account": total_account,
            "symbol": symbols.get(base, "EUR")
        }
        
        return Response(data)



class DashboardAPIView(APIView):
    """
    **ForecastAPIView(APIView)**

    Returns a cashflow forecast plan.

    This API is used by Ajax requests within the Forecast template.
    """
    authenticated_classes = []
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        base = request.GET.get('base', 'EUR').upper()
        nw = Transaction.objects.networth(self.request.user, base)
        crd = Transaction.objects.credits(self.request.user, base )
        deb = Transaction.objects.debits(self.request.user, base)

        months = []
        balance = []
        back = []
        border = []
        
        for m, p in zip(nw['months'], nw['networths']):
            back.append('rgba(1, 1, 1, 0.2)' if p >= 0 else 'rgba(255,99,132,0.2)',)
            border.append('rgba(1, 1, 1, 1)' if p >= 0 else 'rgba(255,99,132,1)',)
         
        data = {
            "bal_labels": nw['months'],
            "bal_data": nw['networths'],
            "bal_back": back,
            "bal_border": border,
            "crd_labels": crd['months'],
            "crd_data": crd['credits'],
            "deb_labels": deb['months'],
            "deb_data": deb['debits'],
        }

        # data = {}
        return Response(data)

