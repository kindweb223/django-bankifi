"""
# Views for Demo Setup
"""

"""
Please note: Hard coded bank accounts (for investors) and contact ids (for loans)
are used in the demo.

Future Work: Remove need for hard coded accounts and contacts.

**View Classes:**

1. ***SetupView***: View to setup the Bankifi Cashflow demo.
2. ***LoggedInView***: View to login to Xero.

Internal Methods:

1. ***clear_loan***: Clear down Bankifi loans.
2. ***clear_invoices***: Clear down Bankifi invoices.
3. ***clear_transactions***: Clear down Bankifi transactions.
4. ***clear_xero_transactions***: Clear down Xero transactions.
5. ***invoices_void***: Void Xero invoices.
"""

# === Imports ===

# Import Python modules
from os import environ
import logging

# Import Django modules
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy

# Import Bankifi/Cashflow models
from cashflow.models import Account, Transaction, Loan, Contact, Invoice

# Import Xero oauth management methods
from utility.xeroutil import get_xero, verify_credentials

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# Setup protected hard coded accounts used in Demo.
# Account IDs for the Supplier and Business accounts. Update if changed.
PROTECTED_ACCOUNT_IDS = [5,6]
PROTECTED_CONTACTS_NAMES = ['A Investor']
# Contact ID for the loan provider. Update if changed.
PROTECTED_CONTACTS = ['3a7ecaea-130f-40ed-a7e3-d381bb0d1b59']

# === Loggers ===

# Setup loggers
infolog = logging.getLogger('infologger')
errorlog = logging.getLogger('prodlogger')


# === Classes ===

class SetupView(LoginRequiredMixin, TemplateView):
    """
    **SetupView(LoginRequiredMixin, TemplateView)**

    View to setup the Bankifi Cashflow demo.
    """
    template_name = "cashflow/setup/setup.html"

    def get_context_data(self, **kwargs):
        context = super(SetupView, self).get_context_data(**kwargs)

        # Clear loans and add counts to context
        context['loan_count'] = clear_loan(self.request.user)
        context['invoice_count'] = clear_invoices(self.request.user)
        context['transaction_count'] = clear_transactions(self.request.user)

        if ON_HEROKU:
            # Create a Xero object that allows access to the API
            xero = get_xero(self.request)
            if xero is not None:
                # Void Xero invoices (this removes bank account transactions too)
                try:
                    context['invoice_void_count'] = invoices_void(xero)
                except:
                    errorlog.error('Xero token expired, or our request was rejected by Xero API.')
                    errorlog.error(sys.exc_info()[0])
                    context['error'] = "Xero token invalid. Log back into Xero."

            else:
                # Log error if we failed to logon to Xero
                errorlog.error('Get xero returned none.')
                context['error'] = "Error connecting to Xero. Check you are logged in."

        return context


class LoggedInView(LoginRequiredMixin, TemplateView):
    """
    **LoggedInView(LoginRequiredMixin, TemplateView)**

    View to login and verify access to Xero.
    """
    # template_name = "cashflow/setup/logged_in.html"
    template_name = "cashflow/setup/logged_in.html"

    def get(self, request, *args, **kwargs):
        context = super(LoggedInView, self).get_context_data(**kwargs)

        if ON_HEROKU:
            # Verify the Xero credentials
            verify_credentials(self.request)

        return redirect(reverse_lazy('cashflow:forecast'), permanent=True)


# === Methods ===

def clear_loan(user):
    """
    **clear_loan()**

    Clears the Bankifi/Cashflow loans.

    **Returns**:

    Number of loans deleted.
    """
    loans = Loan.objects.filter(customer=user)

    for loan in loans:
        loan.delete()

    return loans.count()


def clear_invoices(user):
    """
    **clear_invoices()**

    Clears the Bankifi/Cashflow invoices.

    **Returns:**

    Number of invoices deleted.
    """
    invoices = Invoice.objects.filter(customer=user)

    for invoice in invoices:
        invoice.delete()

    return invoices.count()


def clear_transactions(user):
    """
    **clear_transactions()**

    Clears the Bankifi/Cashflow transactions.

    **Returns:**

    Number of transactions deleted.
    """
    transactions = Transaction.objects.exclude(contact__name__in=PROTECTED_CONTACTS_NAMES).filter(customer=user)

    for transaction in transactions:
        transaction.delete()

    return transactions.count()


def clear_xero_transactions(xero):
    """
    **clear_xero_transactions(xero)**

    Clears the xero transactions.

    Please note: Due to Xero API limitation, can only clear bank transfers. Other transactions need
    to be cleared manually in Xero for now.

    **Returns**:

    Number of transactions deleted.
    """
    transactions = xero.banktransactions.filter(Status='AUTHORISED')
    count = 0
    for transaction in transactions:
        print("TRANSACTION {0} Contact: {1}".format(transaction, transaction.get('Contact', None)))
        # Keep the important Investor transactions to avoid having to set them up manually again
        if transaction.get('Contact', None) \
                and transaction.get('Contact').get('ContactID') not in PROTECTED_CONTACTS:
            transaction['Status'] = 'DELETED'
            xero.banktransactions.save(transaction)
            count += 1

    return count


def invoices_void(xero):
    """
    **invoices_void(xero)**

    Voids the xero invoices.

    **Returns**:

    Number of invoices voided.
    """
    invoices = xero.invoices.filter(Status='AUTHORISED')

    for i in invoices:
        # Need to do this to update Xero object
        i['Status'] = 'VOIDED'
        try:
            xero.invoices.save(i)
        except:
            errorlog.error("Unable to void Xero invoice. See this data for details: {0}".format(i))

    return len(invoices)
