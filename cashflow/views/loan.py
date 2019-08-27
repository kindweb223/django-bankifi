"""
# Loan views

Bankifi Demo Loan views
"""
"""
**View Classes:**

1. ***LoanApplyView***: View to apply for a loan.
2. ***LoanThankyouView***: View to open loan account, transfer funds and thank customer.
3. ***LoanPayView***: View to settle a loan.

**Internal Methods:**

1. ***pay_loan***: pay outstanding loan balance and clear loan.
"""

# === Imports ===

# Import Django modules
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import TemplateView

# Import Bankifi/Cashflow Models
from cashflow.models import Account, Transaction, Loan, Contact

# Import Bankifi/Cashflow View/Form models and methods
from cashflow.views.invoice import make_offer

# Import Xero oauth module
from utility.xeroutil import get_xero

# === Globals ===

# Setup hard coded receivable account and contact for Xero loan
RECEIVABLE_ACCOUNT = '8b5367e1-7fb5-4810-9f69-ddb2b26b68a4'
LOAN_CONTACT = 'A Underwriter'

# === Classes ===

class LoanApplyView(LoginRequiredMixin, TemplateView):
    """
    **LoanApplyView(LoginRequiredMixin, TemplateView)**

    View to apply for a loan.
    """
    template_name = "cashflow/loan/loan_apply.html"

    def get_context_data(self, **kwargs):
        context = super(LoanApplyView, self).get_context_data(**kwargs)

        # Add offer amount and accounts to deposit loan into to context
        context['offer'], context['offer_amount'] = make_offer(self.request.user)
        context['accounts'] = Account.objects.filter(customer=self.request.user).order_by('name')

        return context



class LoanThankyouView(LoginRequiredMixin, TemplateView):
    """
    **LoanThankyouView(LoginRequiredMixin, TemplateView)**

    View to open loan account, transfer funds and thank customer.
    """
    template_name = "cashflow/loan/loan_thankyou.html"

    # TODO: after accepting loan we get HTTP 500 - this happens here, and money doesn't go into selected account
    def post(self, request, *args, **kwargs):
        context = super(LoanThankyouView, self).get_context_data(**kwargs)

        # Add loan amount and account to deposit loan into to context
        amount = float(self.request.GET.get('offer_amount', '0').translate({ord(c): None for c in ' ,'}))
        account = self.request.GET.get('account', '')
        context['offer_amount'] = amount
        context['account'] = account

        # Retrieve deposit account object
        dep_account = Account.objects.filter(customer=request.user, account_number=account).first()

        # Open a loan account
        loan = Loan(customer=request.user, balance=-float(amount), account=dep_account, status=Loan.OUTSTANDING)
        if loan is not None:
            loan.save()
            contact = Contact.objects.filter(name=LOAN_CONTACT).first()
             # Make Transfer of funds from loan account to Bank account
            loan.transfer_funds(request.user, float(amount), get_xero(request), contact.contact_id, dep_account.account_id)

        # Display thank you page
        # return render(request, self.template_name, context)

        request.session['title'] = 'Funds Transfer Complete'
        request.session['description'] = "Thankyou. We have successfully transferred £{} to bank account number: {}.".format(amount, account)
        request.session['status'] =  ''

        return HttpResponseRedirect(reverse_lazy('cashflow:forecast'))




class LoanPayView(LoginRequiredMixin, TemplateView):
    """
    **LoanPayView(LoginRequiredMixin, TemplateView)**

    View to settle a loan.
    """
    template_name = "cashflow/loan/loan_pay.html"

    def post(self, request, *args, **kwargs):
        context = super(LoanPayView, self).get_context_data(**kwargs)

        # Retrieve outstanding loan object
        loan = Loan.objects.filter(customer=request.user, status=Loan.OUTSTANDING).first()

        xero = get_xero(request)

        # Pay the loan and update Bankifi and Xero
        reply = pay_loan(request.user, xero)
        if xero and reply[0]:
            # Display loan paid template if successful
            request.session['title'] = 'Loan Payment Complete'
            request.session['description'] = reply[1]
            request.session['status'] =  ''

            return HttpResponseRedirect(reverse_lazy('cashflow:forecast'))

            # return render(request, self.template_name, context)

        else:
            # Return to invoice list if unsuccessful
            request.session['title'] = 'Loan Payment Failed'
            request.session['description'] = 'You have insufficient funds to clear your loan.'
            request.session['status'] =  ''
            return HttpResponseRedirect(reverse('cashflow:forecast'))

# === Methods ===

def pay_loan(user, xero):
    """
    **pay_loan(xero)**

    Settle outstanding loan.

    **Parameters:**

    ***xero***: Xero connection object.

    **Returns:**

    A tuple with True and message if loan paid successfully or False and '' if unsuccessful.
    """
    loan = Loan.objects.filter(customer=user, status=Loan.OUTSTANDING).first()

    if xero and loan is not None and loan.account.transaction_check(user, -loan.balance) == True:
        # Funds are available to make loan payment, so pay
        contact = Contact.objects.filter(name=LOAN_CONTACT).first()
        old_balance = loan.balance
        loan.pay_loan(user, loan.balance, xero, contact.contact_id, RECEIVABLE_ACCOUNT)
        return (True, "You have successfully paid £{0} off your loan and the balance is now £{1}".format(old_balance, loan.balance))
    else:
        # Funds not available or call to Xero failed so return false
        return (False, '')
