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
from django.db.models import F, Sum, Case, When, FloatField


# Import Aggregate Models
from cashflow.models import Account, Transaction
from .models import Group, Consent
from .forms import AccountModelForm, GroupModelForm, GroupCreateModelForm, ConsentCreateForm, TransactionModelForm, AuthenticateForm

# Import Bankifi/aggregate View/Form models and methods
from django.views.generic import (
        DetailView, 
        ListView, 
        CreateView, 
        UpdateView, 
        DeleteView,
        TemplateView,
    )

from django.views.generic.edit import FormView


# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# === Classes ===

class IndexView(LoginRequiredMixin, TemplateView):
    """
    **IndexView(LoginRequiredMixin, TemplateView)**

    View to display index/homepage and setup aggregate accounts and services.
    """
    template_name = "aggregate/account/account_dashboard.html"


    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)

        # Set the exchange rate cache
        context['title'] = 'Account Dashboard'
        context['parent'] = ''
        context['theurl'] = 'aggregate:accountlist'

        return context


class CreateUserView(LoginRequiredMixin, TemplateView):
    """
    **CreateUserView(LoginRequiredMixin, TemplateView)**

    View to create a user.
    """
    template_name = "aggregate/create_user.html"

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        if ON_HEROKU:
           pass

        return context


class AccountSetupView(LoginRequiredMixin, TemplateView):
    """
    **AccountSetupView(LoginRequiredMixin, TemplateView)**

    View to setup accounts and groups.
    """
    template_name = "aggregate/account/account_setup.html"

    def get_context_data(self, **kwargs):
        context = super(AccountSetupView, self).get_context_data(**kwargs)
        if ON_HEROKU:
           pass

        return context


class ManageConsentView(LoginRequiredMixin, TemplateView):
    """
    **ManageConsentView(LoginRequiredMixin, TemplateView)**

    View to manage user account consent rules.
    """
    template_name = "aggregate/manage_consent.html"

    def get_context_data(self, **kwargs):
        context = super(ManageConsentView, self).get_context_data(**kwargs)
        if ON_HEROKU:
           pass

        return context


class AccountDashboardView(LoginRequiredMixin, TemplateView):
    """
    **AccountDashboardView(LoginRequiredMixin, TemplateView)**

    Account Dashboard view.
    """
    template_name = "aggregate/account/account_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(AccountDashboardView, self).get_context_data(**kwargs)

        # context['networth'] = Transaction.objects.networth_total(self.request.user)
        # context['credits'] = Transaction.objects.credit_total(self.request.user)
        # context['debits'] = Transaction.objects.debit_total(self.request.user)
        context['title'] = 'Account Dashboard'
        context['parent'] = ''
        context['theurl'] = ''

        return context



class AccountCreateView(LoginRequiredMixin, CreateView):
    """
    **AccountCreateView(LoginRequiredMixin, CreateView)**

    View to create an account.
    """
    template_name = "aggregate/snippets/create.html"
    form_class = AccountModelForm
    success_url = reverse_lazy("aggregate:accountlist")

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(AccountCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(AccountCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Account'
        context['parent'] = 'Account List'
        context['theurl'] = 'aggregate:accountlist'

        return context



class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    **AccountDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete an account.
    """
    template_name = "aggregate/snippets/confirm_delete.html"
    model = Account
    success_url = reverse_lazy("aggregate:accountlist")

    def get_context_data(self, *args, **kwargs):
        context = super(AccountDeleteView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Delete Account'
        context['parent'] = 'Account List'
        context['theurl'] = 'aggregate:accountlist'
        context['message'] = 'Are you sure you want to delete the account'

        return context



class AccountDetailView(LoginRequiredMixin, DetailView):
    """
    **AccountDetailView(LoginRequiredMixin, DetailView**

    View to provide details of an account.
    """
    template_name = "aggregate/account/account_detail.html" 

    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)         
            
        return qs 

    def get_context_data(self, *args, **kwargs):
        context = super(AccountDetailView, self).get_context_data(*args, **kwargs)

        context['title'] = 'View Account'
        context['parent'] = 'Account List'
        context['theurl'] = 'aggregate:accountlist'

        return context



class AccountListView(LoginRequiredMixin, ListView):
    """
    **AccountListView(LoginRequiredMixin, ListView)**

    View to provide a list of accounts.
    """
    template_name = "aggregate/account/account_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):

        qs = Account.objects.filter(customer=self.request.user, consent__isnull=False).\
            annotate(current_balance=Sum(
                        Case(When(transaction__amount__isnull=False, then=F('transaction__amount')),
                            default=0, output_field=FloatField())))
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(AccountListView, self).get_context_data(*args, **kwargs)
        
        return context


class AccountAddView(LoginRequiredMixin, TemplateView):
    """
    **AccountAddView(LoginRequiredMixin, UpdateView)**

    View to add an account
    """
    template_name = "aggregate/account/account_add.html"
    # form_class = AccountModelForm

    # def get_queryset(self, *args, **kwargs):
    #     qs = Account.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)      
            
    #     return qs

    # def get_form_kwargs(self):
    #     kwargs = super(AccountUpdateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    **AccountUpdateView(LoginRequiredMixin, UpdateView)**

    View to update an account
    """
    template_name = "aggregate/snippets/update.html"
    form_class = AccountModelForm

    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)      
            
        return qs

    def get_form_kwargs(self):
        kwargs = super(AccountUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, *args, **kwargs):
        context = super(AccountUpdateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Update Account'
        context['parent'] = 'Account List'
        context['theurl'] = 'aggregate:accountlist'

        return context



class AccountTransactionListView(LoginRequiredMixin, ListView):
    """
    **AccountTransactionListView(LoginRequiredMixin, ListView)**

    View to List all transactions.
    """
    template_name = "aggregate/group/group_transaction_list.html"
    
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(customer=self.request.user, account__pk=self.kwargs['pk'])            
        return qs  

    def get_context_data(self, *args, **kwargs):
        context = super(AccountTransactionListView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Group Transaction List'
        context['parent'] = 'Group'
        context['theurl'] = 'aggregate:grouplist'

        return context



class GroupCreateView(LoginRequiredMixin, CreateView):
    """
    **GroupCreateView(LoginRequiredMixin, CreateView)**

    View to create an Group.
    """
    template_name = "aggregate/snippets/create.html"
    form_class = GroupModelForm
    success_url = reverse_lazy("aggregate:grouplist")

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(GroupCreateView, self).form_valid(form)


    def get_form_kwargs(self):
        kwargs = super(GroupCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, *args, **kwargs):
        context = super(GroupCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Group'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context



class GroupDeleteView(LoginRequiredMixin, DeleteView):
    """
    **GroupDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete an Group.
    """
    template_name = "aggregate/snippets/confirm_delete.html"
    model = Group
    success_url = reverse_lazy("aggregate:grouplist")

    def get_context_data(self, *args, **kwargs):
        context = super(GroupDeleteView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Delete Group'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['message'] = 'Are you sure you want to delete the group'

        return context




class GroupDetailView(LoginRequiredMixin, DetailView):
    """
    **GroupDetailView(LoginRequiredMixin, DetailView**

    View to provide details of an Group.
    """
    template_name = "aggregate/group/group_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = Group.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)      
            
        return qs 


    def get_context_data(self, *args, **kwargs):
        context = super(GroupDetailView, self).get_context_data(*args, **kwargs)

        context['title'] = 'View Group'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'

        return context



class GroupListView(LoginRequiredMixin, ListView):
    """
    **GroupListView(LoginRequiredMixin, ListView)**

    View to provide a list of Groups.
    """
    template_name = "aggregate/group/group_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Group.objects.filter(customer=self.request.user).annotate(balance=Sum(F('accounts__transaction__amount')))
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(GroupListView, self).get_context_data(*args, **kwargs)

        return context



class GroupUpdateView(LoginRequiredMixin, UpdateView):
    """
    **GroupUpdateView(LoginRequiredMixin, UpdateView)**

    View to update an Group
    """
    template_name = "aggregate/snippets/update.html"
    form_class = GroupModelForm

    def get_queryset(self, *args, **kwargs):
        qs = Group.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)         
            
        return qs


    def get_form_kwargs(self):
        kwargs = super(GroupUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, *args, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Update Group'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'

        return context



class GroupTransactionListView(LoginRequiredMixin, ListView):
    """
    **GroupTransactionListView(LoginRequiredMixin, ListView)**

    View to List all transactions.
    """
    template_name = "aggregate/group/group_transaction_list.html"
    
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(customer=self.request.user, account__group__pk=self.kwargs['pk'])           
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(GroupTransactionListView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Group Transaction List'
        context['parent'] = 'Group'
        context['theurl'] = 'aggregate:grouplist'

        return context




class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    **TransactionCreateView(LoginRequiredMixin, CreateView)**

    View to create a transaction.
    """
    template_name = "aggregate/snippets/create.html"
    form_class = TransactionModelForm
    success_url = reverse_lazy("aggregate:transactionlist")

    def get_form_kwargs(self):
        kwargs = super(TransactionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(TransactionCreateView, self).form_valid(form)


    def get_context_data(self, *args, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Transaction'
        context['parent'] = 'Transaction List'
        context['theurl'] = 'aggregate:transactionlist'

        return context



class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    **TransactionDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete a transaction.
    """
    template_name = "aggregate/snippets/confirm_delete.html"
    model = Transaction
    success_url = reverse_lazy("aggregate:transactionlist")

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionDeleteView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Delete Transaction'
        context['parent'] = 'Transaction List'
        context['theurl'] = 'aggregate:transactionlist'
        context['message'] = 'Are you sure you want to delete the transaction'

        return context




class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    **TransactionDetailView(LoginRequiredMixin, DetailView)**

    View to provide detail of a transaction.
    """
    template_name = "aggregate/transaction/transaction_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)
            
        return qs     


    def get_context_data(self, *args, **kwargs):
        context = super(TransactionDetailView, self).get_context_data(*args, **kwargs)

        context['title'] = 'View Transaction'
        context['parent'] = 'Transaction List'
        context['theurl'] = 'aggregate:transactionlist'

        return context
  



class TransactionListView(LoginRequiredMixin, ListView):
    """
    **TransactionListView(LoginRequiredMixin, ListView)**

    View to List all transactions.
    """
    template_name = "aggregate/transaction/transaction_list.html"
    
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(customer=self.request.user, account__consent__isnull=False)            
        return qs


    def get_context_data(self, *args, **kwargs):
        context = super(TransactionListView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Transaction List'
        context['parent'] = ''
        context['theurl'] = 'aggregate:transactionlist'

        return context



class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    **TransactionUpdateView(LoginRequiredMixin, UpdateView)**

    View to Update a transaction.
    """
    template_name = "aggregate/snippets/update.html"
    form_class = TransactionModelForm

    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)
            
        return qs

    def get_form_kwargs(self):
        kwargs = super(TransactionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_context_data(self, *args, **kwargs):
        context = super(TransactionUpdateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Update Transaction'
        context['parent'] = 'Transaction List'
        context['theurl'] = 'aggregate:transactionlist'

        return context


class ConsentCreateView(LoginRequiredMixin, FormView):
    """
    **ConsentCreateView(LoginRequiredMixin, CreateView)**

    View to create a Consent.
    """
    template_name = "aggregate/consent/consent_create.html"
    form_class = ConsentCreateForm
    success_url = reverse_lazy("aggregate:accountlist")

    def form_valid(self, form):
        # form.instance.customer = self.request.user
        # Create object hear
        account = Account.objects.filter(account_number=form.cleaned_data['account_number']).first()
        if account:
            con = Consent.objects.get_or_create(customer=self.request.user, account=account)
        
        return super(ConsentCreateView, self).form_valid(form)


    # def get_form_kwargs(self):
    #     kwargs = super(ConsentCreateView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs


    def get_context_data(self, *args, **kwargs):
        context = super(ConsentCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Authorise Account'
        context['parent'] = 'Consent List'
        context['theurl'] = 'aggregate:consentlist'
        context['auth_form'] = AuthenticateForm

        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context


    # def post(self, request, *args, **kwargs):
    #     context = super(ConsentCreateView, self).get_context_data(**kwargs)
    #     # template = reverse_lazy("aggregate:authorise")
    #     # template = "aggregate/consent/authenticate.html"
    #     # return render(request, template, context)
    #     return HttpResponseRedirect(reverse("aggregate:authenticate"))




class ConsentDeleteView(LoginRequiredMixin, DeleteView):
    """
    **ConsentDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete an Consent.
    """
    template_name = "aggregate/snippets/confirm_delete.html"
    model = Consent
    success_url = reverse_lazy("aggregate:accountlist")

    def get_context_data(self, *args, **kwargs):
        context = super(ConsentDeleteView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Delete Consent'
        context['parent'] = 'Consent List'
        context['theurl'] = 'aggregate:consentlist'
        context['message'] = 'Are you sure you want to delete the consent'

        return context

    def get_object(self, queryset=None):
        obj = Consent.objects.filter(pk=self.kwargs['pk'], customer=self.request.user).first()
        if obj:  
            return obj
        else:
            obj = Consent.objects.filter(account__id=self.kwargs['pk'], customer=self.request.user).first()
            return obj




class ConsentDetailView(LoginRequiredMixin, DetailView):
    """
    **ConsentDetailView(LoginRequiredMixin, DetailView**

    View to provide details of an Consent.
    """
    template_name = "aggregate/consent/consent_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = Consent.objects.filter(pk=self.kwargs['pk'], customer=self.request.user)      
            
        return qs 


    def get_context_data(self, *args, **kwargs):
        context = super(ConsentDetailView, self).get_context_data(*args, **kwargs)

        context['title'] = 'View Consent'
        context['parent'] = 'Consent List'
        context['theurl'] = 'aggregate:consentlist'

        return context



class ConsentListView(LoginRequiredMixin, ListView):
    """
    **ConsentListView(LoginRequiredMixin, ListView)**

    View to provide a list of Consents.
    """
    template_name = "aggregate/consent/consent_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Consent.objects.filter(customer=self.request.user)
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ConsentListView, self).get_context_data(*args, **kwargs)

        return context


class AuthenticateView(LoginRequiredMixin, FormView):
    """
    **AuthenticateView(LoginRequiredMixin, DetailView**

    View to provide details of an Consent.
    """
    template_name = "aggregate/consent/authenticate.html"
    form_class = AuthenticateForm

    def get_context_data(self, *args, **kwargs):
        context = super(AuthenticateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'View Consent'
        context['parent'] = 'Consent List'
        context['theurl'] = 'aggregate:consentlist'

        return context

    def post(self, request, *args, **kwargs):
        context = super(AuthenticateView, self).get_context_data(**kwargs)
        # template = reverse_lazy("aggregate:authorise")
        # template = "aggregate/consent/authenticate.html"
        # return render(request, template, context)
        return HttpResponseRedirect(reverse("aggregate:authorise"))


class AuthoriseView(LoginRequiredMixin, TemplateView):
    """
    **AuthoriseView(LoginRequiredMixin, DetailView**

    View to provide details of an Consent.
    """
    template_name = "aggregate/consent/authorise.html"

    # def get_context_data(self, *args, **kwargs):
    #     context = super(AuthoriseView, self).get_context_data(*args, **kwargs)

    #     context['title'] = 'View Consent'
    #     context['parent'] = 'Consent List'
    #     context['theurl'] = 'aggregate:consentlist'

    #     return context



            

