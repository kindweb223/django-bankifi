# -*- coding: utf-8 -*-
from django.shortcuts import render

from datetime import datetime

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from utility.xeroutil import get_xero_credentials, get_xero

from .models import Loan, BankAccount


BANKIFI_CODE='12345'
BFS_CODE='67893'
BFS_NAME='BFS LOAN 3'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "bankxero/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # Login to Xero to generate credentials to access the authorization URL
        credentials = get_xero_credentials(self.request)

        # Setup the authorization URL xero needs to ask the user to provide consent
        context['authorization_url'] = credentials.url

        return context
    


class AuthorizationView(LoginRequiredMixin, TemplateView):
    template_name = "bankxero/authorization.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)

        # # We can now create a Xero object that allows access to the API
        xero = get_xero(self.request)
        context['invoices'] = xero.invoices.filter(Status='AUTHORISED')
        context['offer'], context['offer_amount'] = make_offer(xero.invoices.filter(Status='AUTHORISED'))
        loan = Loan.objects.first()
        if loan:
            context['loan_balance_str'] = "£{0:,}".format(int(loan.balance))
            context['loan_balance'] = int(loan.balance)
        account = BankAccount.objects.first()
        if account:
            context['bank_balance'] = "£{0:,}".format(int(account.balance))


        return context


    def post(self, request, *args, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)
       
        xero = get_xero(self.request)
 
        # Save the payments
        amount = self.request.GET.get('amount').translate({ord(c): None for c in ' ,'})
        xero.payments.put({
                            'Invoice': {'InvoiceNumber': self.request.GET.get('invoice')}, 
                            # Add to Bankifi Bank Account - 12345
                            'Account': {'Code': BANKIFI_CODE}, 
                            'Amount': amount, 
                            'Date': datetime.now().date()
                        })

        # Update shadow bank account balance
        update_balance(float(amount)) 
 
        context['invoices'] = xero.invoices.filter(Status='AUTHORISED')
        context['offer'], context['offer_amount'] = make_offer(xero.invoices.filter(Status='AUTHORISED'))
        context['loan_balance_str'] = "£{0:,}".format(int(Loan.objects.first().balance))
        context['loan_balance'] = int(Loan.objects.first().balance)
        context['bank_balance'] = "£{0:,}".format(int(BankAccount.objects.first().balance))
      
        # Post the payment
        return render(request, self.template_name, context)



class ApplyView(LoginRequiredMixin, TemplateView):
    template_name = "bankxero/apply.html"

    def get_context_data(self, **kwargs):
        context = super(ApplyView, self).get_context_data(**kwargs)

        xero = get_xero(self.request)
        context['offer'], context['offer_amount'] = make_offer(xero.invoices.filter(Status='AUTHORISED'))
        context['accounts'] = xero.accounts.filter(Code=BANKIFI_CODE)

        return context



class ThankyouView(LoginRequiredMixin, TemplateView):
    template_name = "bankxero/thankyou.html"

    def post(self, request, *args, **kwargs):
        context = super(ThankyouView, self).get_context_data(**kwargs)
       
        xero = get_xero(self.request)
        
        context['offer_amount'] = self.request.GET.get('offer_amount')
        context['account'] = self.request.GET.get('account')
        
        # Make Transfer of funds from loan account to Bank account (need to strip commas)
        amount = self.request.GET.get('offer_amount').translate({ord(c): None for c in ' ,'})
        xero.banktransfers.put({
                                'FromBankAccount': {'Code': BFS_CODE}, 
                                'ToBankAccount': {'Code': BANKIFI_CODE},
                                'Amount': amount,
                            })
        # Update shadow bank account balance
        update_balance(float(amount)) 
        update_loan(float(amount)) 
      
        # Post the payment
        return render(request, self.template_name, context)



class PayLoanView(LoginRequiredMixin, TemplateView):
    template_name = "bankxero/payloan.html"

    def post(self, request, *args, **kwargs):
        context = super(PayLoanView, self).get_context_data(**kwargs)
       
        xero = get_xero(self.request)

        xero.banktransfers.put({
                                'FromBankAccount': {'Code': BANKIFI_CODE}, 
                                'ToBankAccount': {'Code': BFS_CODE},
                                'Amount': loan_balance(),
                            })
        # Update shadow bank account balance
        clear_loan() 
          
        # Post the payment
        return render(request, self.template_name, context)



def loan_balance():
    return Loan.objects.first().balance


def update_balance(balance):
    bankaccount = BankAccount.objects.first()
    bankaccount.balance += balance
    bankaccount.save() 


def update_loan(amount):
    loan = Loan.objects.first()
    loan.balance += amount
    loan.save() 


def clear_loan():
    bankaccount = BankAccount.objects.first()
    loan = Loan.objects.first()
    bankaccount.balance -= loan.balance
    loan.balance = 0.0
    bankaccount.save()
    loan.save() 


def make_offer(invoices):
    paid_total = 0.0 
    invoice_total = 0.0
    offer = 0.0
    latest_date = None
    for invoice in invoices:
        invoice_total += invoice.get('Total') if invoice.get('Total') else 0.0
        paid_total += invoice.get('AmountPaid') if invoice.get('AmountPaid') else 0.0
        if latest_date is None or latest_date < invoice.get('DueDateString'):
            latest_date = invoice.get('DueDateString') 

    if latest_date is not None:
        days_to_pay = (latest_date - datetime.now().date()).days
    else:
        days_to_pay = 0

    offer_amt = invoice_total - paid_total
    # interest = offer_amt * 0.002 * days_to_pay
    interest = 0.0

    offer_total = offer_amt + interest

    if days_to_pay > 0:
        return ("Your last invoice is not due until {4}. We can help provide cashflow \
                    and offer you £{0:,} for {1} days. As a special introductory offer, interest would be £{2:,} and total to payback is £{3:,}"\
                    .format(int(offer_amt), days_to_pay, int(interest), int(offer_total), latest_date.strftime("%d %B %Y")), "{0:,}".format(int(offer_amt)))
    else:
        return ("Sorry you have no invoices currently due.", 0.0)


'''
    [{'AmountCredited': 0.0, 
    'UpdatedDateUTC': datetime.datetime(2017, 2, 20, 13, 56, 50, 63000), 
    'LineItems': [], 
    'Reference': '', 
    'CurrencyCode': 'GBP', 
    'InvoiceID': '507c8def-7eeb-4d09-b064-01f92e8416ca', 
    'DueDate': datetime.datetime(2017, 2, 28, 0, 0), 
    'Prepayments': [], 
    'IsDiscounted': False, 
    'TotalTax': 300.0, 
    'InvoiceNumber': 'INV-0001', 
    'AmountDue': 1800.0, 
    'Status': 'AUTHORISED', 
    'Type': 'ACCREC', 
    'Payments': [], 
    'Date': datetime.datetime(2017, 2, 20, 0, 0), 
    'HasAttachments': False, 
    'DateString': datetime.date(2017, 2, 20), 
    'CreditNotes': [], 
    'Total': 1800.0, 
    'DueDateString': datetime.date(2017, 2, 28), 
    'SubTotal': 1500.0, 
    'Contact': {'HasValidationErrors': False, 
                'ContactPersons': [], 
                'Phones': [], 
                'Addresses': [], 
                'Name': 'ACME Bank', 
                'ContactID': '7343f28e-22bd-4c18-99a6-aacda24d36ad', 
                'ContactGroups': []}, 
    'LineAmountTypes': 'Exclusive', 
    'AmountPaid': 0.0, 
    'HasErrors': False, 
    'CurrencyRate': 1.0, 
    'Overpayments': []}] 
'''
    








