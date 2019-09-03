""" 
#Transaction Model Views

Django views basically handle URL requests and routing including passing data to render via templates.
They can handle both HTTP GET and POST requests. This project uses Django class based views.

These views require a user to have logged into the application which is enforced by the LoginRequiredMixin.
"""
"""
View Classes:

1. ***TransactionCreateView***: View to create a transaction.
2. ***TransactionDeleteView***: View to delete a transaction.
3. ***TransactionDetailView***: View to provide a transaction detail.
4. ***TransactionListView***: View to provide a list of transactions.
5. ***TransactionUpdateView***: View to update a transaction.
6. ***TransactionImportView***: View to import transactions from Xero.

Internal Methods:

1. ***add_transaction***: Add a single transaction to Bankifi imported from Xero.
2. ***add_transactions***: Add all transactions to Bankifi imported from Xero.
"""

# Import Python modules
from os import environ
from datetime import date, timedelta, datetime

# Import Django modules
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Import Bankifi/Cashflow views, models and forms
from django.views.generic import (
        DetailView, 
        ListView, 
        CreateView, 
        UpdateView, 
        DeleteView,
        TemplateView,
    )
from cashflow.models import Transaction, Account, Contact
from cashflow.forms import TransactionModelForm


# Import xero oauth management methods
from utility.xeroutil import get_xero

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    **TransactionCreateView(LoginRequiredMixin, CreateView)**

    View to create a transaction.
    """
    template_name = "cashflow/transaction/transaction_create.html"
    form_class = TransactionModelForm
    success_url = reverse_lazy("cashflow:transactionlist")

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(TransactionCreateView, self).form_valid(form)
    def get_context_data(self, *args, **kwargs):
        context = super(TransactionCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Transaction'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    **TransactionDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete a transaction.
    """
    template_name = "cashflow/transaction/transaction_confirm_delete.html"
    model = Transaction
    success_url = reverse_lazy("cashflow:transactionlist")



class TransactionDetailView(LoginRequiredMixin, DetailView):
    """
    **TransactionDetailView(LoginRequiredMixin, DetailView)**

    View to provide detail of a transaction.
    """
    template_name = "cashflow/transaction/transaction_detail.html"
    queryset = Transaction.objects.all()



class TransactionListView(LoginRequiredMixin, ListView):
    """
    **TransactionListView(LoginRequiredMixin, ListView)**

    View to List all transactions.
    """
    template_name = "cashflow/transaction/transaction_list.html"
    
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(customer=self.request.user)            
        return qs

    # Setup authorization URL required for Xero
    def get_context_data(self, *args, **kwargs):
            context = super(TransactionListView, self).get_context_data(*args, **kwargs)
            context['authorization_url'] = reverse_lazy("cashflow:transactionimport")
            
            return context



class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    **TransactionUpdateView(LoginRequiredMixin, UpdateView)**

    View to Update a transaction.
    """
    template_name = "cashflow/transaction/transaction_update.html"
    form_class = TransactionModelForm

    def get_queryset(self, *args, **kwargs):
        qs = Transaction.objects.filter(customer=self.request.user)            
        return qs



class TransactionImportView(LoginRequiredMixin, TemplateView):
    """
    **TransactionImportView(LoginRequiredMixin, TemplateView)**

    View to Import Transactions from Xero.
    """
    template_name = "cashflow/transaction/transaction_import.html"

    # Import the transactions from Xero and add the number imported to the context
    def get_context_data(self, **kwargs):
        context = super(TransactionImportView, self).get_context_data(**kwargs)
        
        if ON_HEROKU:
            # create a Xero object that allows access to the API
            xero = get_xero(self.request)
            # Add transactions to Bankifi and add count to context
            context['add_count'] = add_transactions(xero, self.request.user)
        
        return context


# === Methods ===

def add_transaction(transaction, user):
    """
    **add_transaction(transaction)**

    Add a single transaction to Bankifi imported from Xero.

    **Parameters:**

    ***transaction***: A transaction dictionary containing Xero transaction information.

    **Returns**:

    1 if transaction updated or 0 if not.
    """
    count = 0
    bf_transaction = Transaction.objects.filter(transaction_id=transaction.get('BankTransactionID', '')).first()
    if bf_transaction is None:
        account = Account.objects.filter(account_id=transaction.get('BankAccount','').get('AccountID', '')).first()
        contact = Contact.objects.filter(contact_id=transaction.get('Contact','').get('ContactID', '')).first()
        trans_type = Transaction.CREDIT if transaction.get('Type','') == 'RECEIVE' else Transaction.DEBIT
        bf_transaction = Transaction(
                customer=user,
                account=account,
                transaction_type=trans_type,
                amount=transaction.get('Total', 0.0),
                description="{0} from {1}".format(trans_type, transaction.get('Contact','').get('Name', '') ),
                contact=contact,
                transdate=transaction.get('Date', datetime.now()),
                transaction_id=transaction.get('BankTransactionID', ''),
            )
        if bf_transaction:
            bf_transaction.save()
            count = 1

    return count


def add_transactions(xero, user):
    """
    **add_transactions(xero)**

    Add imported Xero transactions to Bankifi.

    **Parameters:**

    ***xero***: Xero connection object.

    **Returns:**

    Number of transactions added to Bankifi.
    """
    transactions = xero.banktransactions.filter(Status='AUTHORISED')
    count = 0
    
    for transaction in transactions:
        count += add_transaction(transaction, user) 

    return count
