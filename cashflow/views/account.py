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

# === Imports ===

# Import Python modules
from os import environ

# Import Django modules
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import F, Sum, Case, When, FloatField


# Import Bankifi/Cashflow Models
from cashflow.models import Account 

# Import Bankifi/Cashflow View/Form models and methods
from django.views.generic import (
        DetailView, 
        ListView, 
        CreateView, 
        UpdateView, 
        DeleteView,
        TemplateView,
    )
from cashflow.forms import AccountModelForm

# Import Xero oauth module
from utility.xeroutil import get_xero

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')


# === Classes ===

class AccountCreateView(LoginRequiredMixin, CreateView):
    """
    **AccountCreateView(LoginRequiredMixin, CreateView)**

    View to create an account.
    """
    template_name = "cashflow/account/account_create.html"
    form_class = AccountModelForm
    success_url = reverse_lazy("cashflow:accountlist")

    def get_form_kwargs(self):
        kwargs = super(AccountCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, *args, **kwargs):
        context = super(AccountCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Sandbox Account'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(AccountCreateView, self).form_valid(form)



class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    **AccountDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete an account.
    """
    template_name = "cashflow/account/account_confirm_delete.html"
    model = Account
    success_url = reverse_lazy("cashflow:accountlist")



class AccountDetailView(LoginRequiredMixin, DetailView):
    """
    **AccountDetailView(LoginRequiredMixin, DetailView**

    View to provide details of an account.
    """
    template_name = "cashflow/account/account_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(customer=self.request.user)
            
        return qs



class AccountListView(LoginRequiredMixin, ListView):
    """
    **AccountListView(LoginRequiredMixin, ListView)**

    View to provide a list of accounts.
    """
    template_name = "cashflow/account/account_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(customer=self.request.user).\
            annotate(account_balance=Sum(
                        Case(When(transaction__amount__isnull=False, transaction__customer=self.request.user, then=F('transaction__amount')),
                            default=0, output_field=FloatField())))
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(AccountListView, self).get_context_data(*args, **kwargs)
        
        return context



class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    **AccountUpdateView(LoginRequiredMixin, UpdateView)**

    View to update an account
    """
    template_name = "cashflow/account/account_update.html"
    form_class = AccountModelForm

    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(customer=self.request.user)
            
        return qs



class AccountImportView(LoginRequiredMixin, TemplateView):
    """
    **AccountImportView(LoginRequiredMixin, TemplateView)**

    View to import Bankifi/Cashflow accounts from Xero.
    """ 
    template_name = "cashflow/account/account_import.html"

    def get_context_data(self, **kwargs):
        context = super(AccountImportView, self).get_context_data(**kwargs)
        
        if ON_HEROKU:
            # We can now create a Xero object that allows access to the API
            xero = get_xero(self.request)
            context['add_count'] = add_accounts(self.request.user, xero)
        
        return context


# === Methods ===

def add_account(user, account):
    """
    **add_account(account)**

    Add an imported account from Xero

    **Parameters:**

    ***account***: Xero account to add to Bankifi.

    **Returns:**

    1 if account was added or 0 if account was not added.
    """ 
    count = 0
    bf_account = Account.objects.filter(customer=user, account_id=account.get('AccountID', '')).first()
    if bf_account is None:
        accnum = account.get('BankAccountNumber', '').replace('-', '')              
        bf_account = Account(customer=user, bank=account.get('Type', ''), name=account.get('Name', ''), 
            sortcode=accnum[:6],
            account_number=accnum[6:15], account_id=account.get('AccountID', ''))
        if bf_account:
            bf_account.save()
            count = 1

    return count


def add_accounts(user, xero):
    """
    **add_accounts(xero)**

    Add a list of imported accounts from Xero 

    **Parameters:**

    ***xero***: Xero connection object

    **Returns:**

    Number of accounts added to Bankifi
    """ 
    accounts = xero.accounts.filter(Status='ACTIVE', Type='BANK')
    count = 0
    
    for account in accounts:
        count += add_account(user, account) 

    return count
