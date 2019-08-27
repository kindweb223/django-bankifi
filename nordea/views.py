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
        DetailView, 
        ListView, 
        CreateView, 
        UpdateView, 
        DeleteView,
        TemplateView,
    )

from .forms import ContactModelForm, AccountModelForm, TransactionModelForm

from nordea.helpers import nordea_api, get_currency
from nordea.breakdown import get_breakdown
# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# === Classes ===

class IndexView(LoginRequiredMixin, TemplateView):
    """
    **IndexView(LoginRequiredMixin, TemplateView)**

    View to display index/homepage and setup Xero credentials URL.
    """
    template_name = "nordea/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if ON_HEROKU:
           pass

        return context
            

"""
# Account Views

Django Views for Account Model
"""
"""

**View Classes:**

1. ***AccountCreateView***: View to create an account.
2. ***AccountDeleteView***: View to delete an account.
3. ***AccountDetailView***: View to provide details of an account.
4. ***AccountListView***: View to provide a list of accounts.
5. ***AccountUpdateView***: View to update an account.
6. ***AccountImportView***: View to import accounts from Xero.

**Internal Methods:**

1. ***add_accounts***: Add all accounts to Bankifi imported from Xero.
2. ***add_account***: Add a account to Bankifi imported from Xero.

"""

# === Classes ===

class AccountCreateView(LoginRequiredMixin, CreateView):
    """
    **AccountCreateView(LoginRequiredMixin, CreateView)**

    View to create an account.
    """
    template_name = "nordea/account_create.html"
    form_class = AccountModelForm
    success_url = reverse_lazy("nordea:accountlist")



class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    **AccountDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete an account.
    """
    template_name = "nordea/account_confirm_delete.html"
    model = Account
    success_url = reverse_lazy("nordea:accountlist")



class AccountDetailView(LoginRequiredMixin, DetailView):
    """
    **AccountDetailView(LoginRequiredMixin, DetailView**

    View to provide details of an account.
    """
    template_name = "nordea/account_detail.html"
    queryset = Account.objects.all()



class AccountListView(LoginRequiredMixin, ListView):
    """
    **AccountListView(LoginRequiredMixin, ListView)**

    View to provide a list of accounts.
    """
    template_name = "nordea/account_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.all()    
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(AccountListView, self).get_context_data(*args, **kwargs)
        
        return context



class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    **AccountUpdateView(LoginRequiredMixin, UpdateView)**

    View to update an account
    """
    template_name = "nordea/account_update.html"
    queryset = Account.objects.all()
    form_class = AccountModelForm


# === Classes ===

class ContactCreateView(LoginRequiredMixin, CreateView):
    """
    **ContactCreateView(LoginRequiredMixin, CreateView)**

    View to create a Bankifi/Cashflow contact.
    """ 
    template_name = "nordea/contact_create.html"
    form_class = ContactModelForm
    success_url = reverse_lazy("nordea:contactlist")



class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """
    **ContactDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete a Bankifi/Cashflow contact.
    """ 
    template_name = "nordea/contact_confirm_delete.html"
    model = Contact
    success_url = reverse_lazy("nordea:contactlist")



class ContactDetailView(LoginRequiredMixin, DetailView):
    """
    **ContactDetailView(LoginRequiredMixin, DetailView)**

    View to view details of a Bankifi/Cashflow contact.
    """ 
    template_name = "nordea/contact_detail.html"
    queryset = Contact.objects.all()



class ContactListView(LoginRequiredMixin, ListView):
    """
    **ContactListView(LoginRequiredMixin, ListView)**

    View to display list of Bankifi/Cashflow contacts.
    """ 
    template_name = "nordea/contact_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Contact.objects.all()    
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ContactListView, self).get_context_data(*args, **kwargs)
        # Add URL shortcuts to allow create, update and delete from list view
        context['create_url'] = reverse_lazy('nordea:contactcreate')
        context['update_url'] = reverse_lazy('nordea:contactupdate')
        context['delete_url'] = reverse_lazy('nordea:contactdelete')
        return context



class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """
    **ContactUpdateView(LoginRequiredMixin, UpdateView)**

    View to update a Bankifi/Cashflow contact.
    """ 
    template_name = "contact_update.html"
    queryset = Contact.objects.all()
    form_class = ContactModelForm
    success_url = reverse_lazy("nordea:contactlist")



class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    **TransactionCreateView(LoginRequiredMixin, CreateView)**

    View to create a transaction.
    """
    template_name = "nordea/transaction_create.html"
    form_class = TransactionModelForm
    success_url = reverse_lazy("nordea:transactionlist")



class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    **TransactionDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete a transaction.
    """
    template_name = "nordea/transaction_confirm_delete.html"
    model = Transaction
    success_url = reverse_lazy("nordea:transactionlist")



class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    **TransactionDetailView(LoginRequiredMixin, DetailView)**

    View to provide detail of a transaction.
    """
    template_name = "nordea/transaction_detail.html"
    queryset = Transaction.objects.all()



class TransactionListView(LoginRequiredMixin, ListView):
    """
    **TransactionListView(LoginRequiredMixin, ListView)**

    View to List all transactions.
    """
    template_name = "nordea/transaction_list.html"
    
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.all()            
        return qs

    # Setup authorization URL required for Xero
    def get_context_data(self, *args, **kwargs):
            context = super(TransactionListView, self).get_context_data(*args, **kwargs)
            context['authorization_url'] = reverse_lazy("nordea:transactionimport")
            
            return context



class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    **TransactionUpdateView(LoginRequiredMixin, UpdateView)**

    View to Update a transaction.
    """
    template_name = "nordea/transaction_update.html"
    queryset = Transaction.objects.all()
    form_class = TransactionModelForm




'''
Provides a list of customer accounts and detailed information across banks
'''
class NordeaAccountView(LoginRequiredMixin, TemplateView):
    template_name = "nordea/view_accounts.html"

    def get_context_data(self, **kwargs):
        context = super(NordeaAccountView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        url_tail =  "/accounts"

        r = nordea_api(url_tail)

        if r.get('content', None) is not None:
            accounts = r.get('content', None)['response']['accounts']
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        account_list = []
        # account_transactions = {}
        # for account in accounts:
        #     # Call get_account_by_id to get balance and other info using bank_id and account id
        #     url_tail = "/accounts/{0}/transactions".format(account.get('id'))
        #     details = nordea_api(url_tail)

        #     # Some of the accounts are not accessible so we filter them out
        #     if details is not None:
        #         account_transactions[account.get('id')] = details['response']['transactions']

        context['accounts'] = accounts
        reply = get_currency(['GBP', 'USD']) 
        context['GBP'] = reply.get('GBP', 0.0)
        context['USD'] = reply.get('USD', 0.0)
        # context['account_transactions'] = account_transactions


        return context


'''
Provides a list of customer accounts and detailed information across banks
'''
class NordeaTransactionView(LoginRequiredMixin, TemplateView):
    template_name = "nordea/view_transactions.html"

    def get_context_data(self, **kwargs):
        context = super(NordeaTransactionView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        pk = self.kwargs.get('pk', None)
        context['pk'] = pk
        url_tail = "/accounts/{0}/transactions".format(pk)

        r = nordea_api(url_tail)

        if r.get('content', None) is not None:
            context['transactions'] = r.get('content', None)['response']['transactions']
            context['account'] = r.get('content', None)['response']['account']
            reply = get_currency(['GBP', 'USD']) 
            context['GBP'] = reply.get('GBP', 0.0)
            context['USD'] = reply.get('USD', 0.0)
        else:
            context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        return context


'''
Provides a list of customer accounts and detailed information across banks
'''
class NordeaBreakdownView(LoginRequiredMixin, TemplateView):
    template_name = "nordea/breakdown.html"

    def get_context_data(self, **kwargs):
        context = super(NordeaBreakdownView, self).get_context_data(**kwargs)

        # Need to call this API to get list of current user accounts
        # pk = self.kwargs.get('pk', None)
        # context['pk'] = pk

        breakdown = get_breakdown()

        context['money_in'] = breakdown.get('credits', 0.0)
        context['money_out'] = breakdown.get('debits', 0.0)
        context['money_total'] = breakdown.get('total', 0.0)

        context['title'] = 'Account Dashboard'
        context['parent'] = ''
        context['theurl'] = ''


        # url_tail = "/accounts/{0}/transactions".format(pk)

        # r = nordea_api(url_tail)

        # if r.get('content', None) is not None:
        #     context['transactions'] = r.get('content', None)['response']['transactions']
        #     context['account'] = r.get('content', None)['response']['account']
        #     reply = get_currency(['GBP', 'USD']) 
        #     context['GBP'] = reply.get('GBP', 0.0)
        #     context['USD'] = reply.get('USD', 0.0)
        # else:
        #     context["error"] = "Error: {0} Msg: {1}".format(r.get('error', "").get('code', ""), r.get('error', "").get('description', ""))

        return context

