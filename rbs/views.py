from django.shortcuts import render

# Create your views here.
"""
# Views for Index

Django Views for Index (Demo Home Page)
"""
""" 
**View Classes:**

1. ***IndexView***: View to display index/homepage and setup Xero credentials URL.
2. ***AuthorizeView***: View to display successful login to Xero message.
"""

# === Imports ===
from os import environ

# Import Django modules

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Import Bankifi/Cashflow Models
from nordea.models import Contact, Account, Transaction

# Import Bankifi/Cashflow View/Form models and methods
from django.views.generic import (
        TemplateView,
    )

from .helpers import bank_api, get_currency
from .breakdown import get_breakdown
# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# === Classes ===

class IndexView(LoginRequiredMixin, TemplateView):
    """
    **IndexView(LoginRequiredMixin, TemplateView)**

    View to display index/homepage and setup Xero credentials URL.
    """
    template_name = "rbs/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if ON_HEROKU:
           pass

        return context
          

'''
Provides a list of customers 
'''
class CustomerView(LoginRequiredMixin, TemplateView):
    template_name = "rbs/view_customers.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        url_tail =  "/customers"

        r = bank_api(url_tail)

        if r.get('content', None) is not None:
            context['customers'] = r.get('content', None).get('results', "")
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        return context


'''
Provides a list of customer accounts and detailed information across banks
'''
class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "rbs/view_accounts.html"

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk
        url_tail =  "/accounts/{0}".format(pk)

        r = bank_api(url_tail)

        if r.get('content', None) is not None:
            context['account'] = r.get('content', None)
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        reply = get_currency(['GBP', 'USD']) 
        context['GBP'] = reply.get('GBP', 0.0)
        context['USD'] = reply.get('USD', 0.0)

        print(context)

        return context


'''
Provides a list of customer accounts and detailed information across banks
'''
class CustomerAccountView(LoginRequiredMixin, TemplateView):
    template_name = "rbs/view_customeraccounts.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerAccountView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk
        url_tail =  "/customers/{0}/accounts".format(pk)

        r = bank_api(url_tail)

        if r.get('content', None) is not None:
            context['accounts'] = r.get('content', None).get('results', "")
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        reply = get_currency(['GBP', 'USD']) 
        context['GBP'] = reply.get('GBP', 0.0)
        context['USD'] = reply.get('USD', 0.0)

        return context


'''
Provides a list of customer accounts and detailed information across banks
'''
class TransactionView(LoginRequiredMixin, TemplateView):
    template_name = "rbs/view_transactions.html"

    def get_context_data(self, **kwargs):
        context = super(TransactionView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk
        url_tail = "/accounts/{0}/transactions".format(pk)

        r = bank_api(url_tail)

        if r.get('content', None) is not None:
            context['transactions'] = r.get('content', None).get('results', "")
            reply = get_currency(['GBP', 'USD']) 
            context['GBP'] = reply.get('GBP', 0.0)
            context['USD'] = reply.get('USD', 0.0)
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        return context



'''
Provides a list of customer accounts and detailed information across banks
'''
class BreakdownView(LoginRequiredMixin, TemplateView):
    template_name = "rbs/breakdown.html"

    def get_context_data(self, **kwargs):
        context = super(BreakdownView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk

        breakdown = get_breakdown(pk)

        context['money_in'] = breakdown.get('credits', 0.0)
        context['money_out'] = breakdown.get('debits', 0.0)
        context['money_total'] = breakdown.get('total', 0.0)

        return context

