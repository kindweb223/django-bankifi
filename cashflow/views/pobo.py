"""
# POBO Views

Bankifi Demo Pay On Behalf Of (POBO) views
"""
"""
**View Classes:**

1. ***PoboCreateView***: View to create a payment request.
2. ***PoboPayView***: View to display the invoice awaiting payment.
3. ***PoboPaymentView***: View to pay an invoice.
4. ***PoboThankyouView***: View to thank customer following payment.
"""

# === Imports ===

# Import Python modules
from datetime import date, timedelta, datetime
from os import environ
import logging
from random import choice, randrange

# Import Django modules
from django.views.generic import CreateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.db.models import F, Sum, Case, When, FloatField


# Import Bankifi/Cashflow Models
from cashflow.models import Invoice, Account, Loan

# Import Bankifi/Cashflow View/Form models and methods
from cashflow.views.invoice import make_offer
from cashflow.views.loan import pay_loan
from cashflow.forms import (
        InvoiceModelForm,
        InvoicePayForm
    )

# Import Xero oauth module
from utility.xeroutil import get_xero

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# N.B. avoid hardcoding deployment config
BANKIFI_ROOT = environ.get('BANKIFI_ROOT')

# === Loggers ===

# Setup loggers
infolog = logging.getLogger('infologger')
errorlog = logging.getLogger('prodlogger')

# === Classes ===

class PoboCreateView(LoginRequiredMixin, CreateView):
    """
    **PoboCreateView(LoginRequiredMixin, CreateView)**

    View to create a payment request.

    Allows a supplier to send an invoice to a Xero business user containing a link for payment.
    """
    template_name = "cashflow/pobo/pobo_create.html"
    form_class = InvoiceModelForm
    model = Invoice
    success_url = reverse_lazy("cashflow:forecast")

    def get_form_kwargs(self):
        kwargs = super(PoboCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, *args, **kwargs):
        context = super(PoboCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Xero Invoice'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context
    # Override form valid method
    def form_valid(self, form):
        infolog.info("IN POBOCREATEVIEW - FORM VALID")
        if ON_HEROKU:
            # Create a Xero object that allows access to the API
            xero = get_xero(self.request)
            infolog.info("Form Valid {0}".format(xero))
            form.instance.customer = self.request.user

            self.object = form.save(commit = False)
            self.object.number = "BI-INV-{0}-{1}-{2}".format(randrange(10000), randrange(10000), randrange(100))
            self.object.save()

            # Setup Xero invoice dictionary
            invoice = {
                    'InvoiceNumber': self.object.number,
                    'Type': 'ACCPAY' if form.cleaned_data.get('invoice_type', '') == Invoice.PAYABLE else 'ACCREC',
                    'LineItems': [{'Description': 'For Services Rendered',
                        'Quantity': '1.0', 'UnitAmount': form.cleaned_data.get('amount', '0.0'), 'AccountCode':'310'}],
                    'Url': '{0}/cashflow/pobo/pay?number={1}'.format(BANKIFI_ROOT, self.object.number),
                    'Contact': {'ContactID': form.cleaned_data.get('contact', '').contact_id},
                    'Date': form.cleaned_data.get('raised', ''),
                    'DueDate': form.cleaned_data.get('due', ''),
                    'LineAmountTypes': 'Inclusive',
                    'Status': 'AUTHORISED'
                }

            # Call Xero api to add invoice
            try:
                result = xero.invoices.put(invoice)
                infolog.info("Result of xero.invoices.put(invoice) in pobo.py: {0}".format(result))
            except:
                errorlog.error("Unable to put new invoice into Xero app. Check log above for more details.")
                errorlog.error(sys.exc_info()[0])

        return super(PoboCreateView, self).form_valid(form)



class PoboPayView(LoginRequiredMixin,  ListView):
    """
    **PoboPayView(LoginRequiredMixin,  ListView)**

    Displays the invoice awaiting payment.
    """
    template_name = "cashflow/pobo/pobo_pay.html"
    model = Invoice

    def get_context_data(self, **kwargs):
        context = super(PoboPayView, self).get_context_data(**kwargs)
        context['number'] = self.request.GET.get('number', '')
        infolog.info("Context: {0}".format(context))
        context['authorization_url'] = reverse_lazy("cashflow:pobopayment")

        return context


    def get_queryset(self, *args, **kwargs):
        qs = Invoice.objects.filter(customer=self.request.user, number=self.request.GET.get('number', ''))
        return qs



class PoboPaymentView(LoginRequiredMixin,  ListView):
    """
    **PoboPaymentView(LoginRequiredMixin,  ListView)**

    Processes the Payment for the Link Sent In.

    Allows the Xero user to pay the bill and update their Xero Bank Account, as well as
    the supplier bank account enabled by Bankifi.
    """
    template_name = "cashflow/pobo/pobo_payment.html"

    # Add invoice number to the context
    def get_context_data(self, **kwargs):
        context = super(PoboPaymentView, self).get_context_data(**kwargs)
        context['number'] = self.request.GET.get('number')

        return context


    def get_queryset(self, *args, **kwargs):
        qs = Account.objects.filter(customer=self.request.user, name='Business Account').\
            annotate(account_balance=Sum(
                        Case(When(transaction__amount__isnull=False, transaction__customer=self.request.user, then=F('transaction__amount')),
                            default=0, output_field=FloatField())))
        return qs


    def post(self, request, *args, **kwargs):
        """
        **post(self, request, *args, **kwargs)**

        Pay invoice and redirect to thankyou page.
        Mark the invoice as paid on Xero and Bankifi.
        Raise Debit and Credit Transaction on Xero and Bankif.
        Potentially offer loan if insufficient funds to pay invoice.
        """
        xero = get_xero(request)
        number = request.GET.get('number', '')
        account = request.GET.get('account', '')

        if xero and request.GET.get('number', ''):
            invoices = xero.invoices.filter(InvoiceNumber=number, Status='AUTHORISED')
        else:
            errorlog.error("Xero check failed {0} {1}".format(xero, number))
            raise Http404("Failed to connect to Xero. Ensure you are signed in.")


        # Pay Xero and Put txn to Xero
        try:
            invoice = invoices[0]
            bk_invoice = Invoice.objects.filter(customer=request.user, number=invoice.get('InvoiceNumber')).first()
            bk_invoice.pay(request.user, account, xero)
        # Exception will occur if insufficient funds
        except ValidationError as e:
            context = {}
            context['number'] = request.GET.get('number', '')
            context['error'] = ",".join(e)
            context['object_list'] = self.queryset
            # If insufficient funds check if a loan offer can be generated
            context['offer'], context['offer_amount'] = make_offer(request.user)
            # Check if loan already in use
            loan = Loan.objects.filter(customer=request.user, status=Loan.OUTSTANDING).first()
            if loan is not None:
                context['loan'] = loan
                context['has_a_loan'] = True
            else:
                context['has_a_loan'] = False
            errorlog.error("Pobopayment failed {0}".format(context))

            # Return to payment view and notify with error and offer loan if available
            return render(request, self.template_name, context)
        except:
            errorlog.error("Pobopayment failed.")
            raise Http404("Failed to make a payment as couldn't retrieve invoices from Xero.")

        if ON_HEROKU:
            xero = get_xero(self.request)
            # context['loan_status'] = pay_loan(xero)[1]
            request.session['title'] = 'Payment Complete'
            request.session['description'] = 'Thankyou. We have successfully completed your payment.'
            request.session['status'] =  pay_loan(request.user, xero)[1]
        return HttpResponseRedirect(reverse('cashflow:forecast'))
        # return HttpResponseRedirect('thankyou')




class PoboThankyouView(LoginRequiredMixin, TemplateView):
    """
    **PoboThankyouView(LoginRequiredMixin, TemplateView)**

    View to display thankyou page and details if a loan has been paid of automatically.
    """
    template_name = "cashflow/pobo/pobo_thankyou.html"
    template_name = "cashflow/pobo/pobo_thankyou.html"

    def get_context_data(self, **kwargs):
        context = super(PoboThankyouView, self).get_context_data(**kwargs)
        if ON_HEROKU:
            xero = get_xero(self.request)
            # context['loan_status'] = pay_loan(xero)[1]
            message = {'title': 'Payment Complete',
                        'description': 'Thankyou. We have successfully completed your payment.',
                        'status': pay_loan(xero)[1]
            }

        return context
