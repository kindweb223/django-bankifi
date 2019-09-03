"""
# Invoice Views

Django Views for Invoice Model
"""
"""
***View Classes***

1. ***InvoiceCreateView*** - View to create an invoice
2. ***InvoiceDeleteView*** - View to delete an invoice
3. ***InvoiceDetailView*** - View to provide an invoice detail
4. ***InvoiceListView*** - View to provide a list of invoices
5. ***InvoiceUpdateView*** - View to update an invoice
6. ***InvoiceImportView*** - View to import invoices from Xero
7. ***InvoiceGenerateView*** - View to generate a random set of invoices
8. ***InvoiceGeneratedView*** - View to show random invoices generated

***Internal Methods***

1. ***make_offer*** - Make a loan offer to pay for an invoice
2. ***add_invoices*** - Add all invoices to Bankifi imported from Xero
3. ***generate_invoices*** - Generate a set of random invoices
4. ***generate_random_invoices*** - Generate a random invoice
"""

# === Imports ===

# Import Python modules
from os import environ
from datetime import date, timedelta, datetime
from random import choice, randrange
import logging

# Import Django modules
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.db.models import Sum

# Import Bankifi/Cashflow Models
from cashflow.models import Invoice, Loan, Contact, Account
from cashflow.views.setup import clear_transactions, clear_invoices

# Import Bankifi/Cashflow View/Form models and methods
from cashflow.views.contact import add_contact, add_contacts
from django.views.generic import (
        DetailView,
        ListView,
        CreateView,
        UpdateView,
        DeleteView,
        TemplateView,
    )

from cashflow.forms import (
        InvoiceModelForm,
        InvoicePayForm,
        InvoiceGenerateForm,
    )

# Import application utility methods
from cashflow.utilities import *

# Import Xero oauth module
from utility.xeroutil import get_xero

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# Setup hard coded receivable and payable account for supplier payments
PAYABLE_ACCOUNT = '45674523'
RECEIVABLE_ACCOUNT = '8b5367e1-7fb5-4810-9f69-ddb2b26b68a4'

# === Loggers ===

# Setup loggers
infolog = logging.getLogger('infologger')
errorlog = logging.getLogger('prodlogger')

# === Invoice View Classes ===

# === Classes ===

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    """
    **InvoiceCreateView(LoginRequiredMixin, CreateView)**

    Create a Bankifi/Cashflow invoice
    """
    template_name = "cashflow/invoice/invoice_create.html"
    form_class = InvoiceModelForm
    success_url = reverse_lazy("cashflow:forecast")

    def get_form_kwargs(self):
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def get_context_data(self, *args, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(*args, **kwargs)

        context['title'] = 'Create Account'
        context['parent'] = 'Group List'
        context['theurl'] = 'aggregate:grouplist'
        context['help_text'] = 'Hold down "Control", or "Command" on a Mac, to select more than one.'
        # context['action_url'] = reverse_lazy('aggregate:groupcreate')

        return context
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(InvoiceCreateView, self).form_valid(form)



class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    """
    **InvoiceDeleteView(LoginRequiredMixin, DeleteView)**

    The class is used to delete a Bankifi/Cashflow invoice
    """
    template_name = "cashflow/invoice/invoice_confirm_delete.html"
    model = Invoice
    success_url = reverse_lazy("cashflow:invoicelist")



class InvoiceDetailView(LoginRequiredMixin, DetailView):
    """
    **InvoiceDetailView(LoginRequiredMixin, DetailView)**

    The class is used to display the details of a Bankifi/Cashflow invoice
    """
    template_name = "cashflow/invoice/invoice_detail.html"

    def get_queryset(self, *args, **kwargs):
        qs = Invoice.objects.filter(customer=self.request.user)

        return qs



class InvoiceListView(LoginRequiredMixin, ListView):
    """
    **InvoiceListView(LoginRequiredMixin, ListView)**

    The class is used to display a list of Bankifi/Cashflow invoices
    """
    template_name = "cashflow/invoice/invoice_list.html"

    def get_context_data(self, **kwargs):
        """
        **get_context_data(self, **kwargs)**

        Override the method to setup additional context data.
        """
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        context['authorization_url'] = reverse_lazy("cashflow:invoiceimport")

        # Check if loan offer available
        context['offer'], context['offer_amount'] = make_offer(self.request.user)
        loan = Loan.objects.filter(customer=self.request.user, status=Loan.OUTSTANDING).first()
        if loan is not None:
            context['loan'] = loan
            context['has_a_loan'] = True
            context['account_balance'] = loan.account.balance(self.request.user)
        else:
            context['has_a_loan'] = False

        return context

    def get_queryset(self, *args, **kwargs):
        """
        **get_queryset(self, *args, **kwargs)**

        Override the method to retrieve a list of invoice objects.
        """
        qs = Invoice.objects.filter(customer=self.request.user)

        return qs


    def post(self, request, *args, **kwargs):
        """
        **post(self, request, *args, **kwargs)**

        Override the method to route a payment request to the 'cashflow/views/pobo.py' module
        """
        invoice = Invoice.objects.get(customer=request.user, pk=int(self.request.GET.get('invoice')))

        url = reverse('cashflow:pobopay')
        return HttpResponseRedirect(url + '?number={0}'.format(invoice.number))



class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    """
    **InvoiceUpdateView(LoginRequiredMixin, UpdateView)**

    The class is used to update a Bankifi/Cashflow invoice.
    """
    form_class = InvoiceModelForm
    template_name = "cashflow/invoice/invoice_update.html"

    def get_queryset(self, *args, **kwargs):
        """
        **get_queryset(self, *args, **kwargs)**

        Override the method to retrieve a list of invoice objects.
        """
        qs = Invoice.objects.filter(customer=self.request.user)

        return qs



class InvoiceImportView(LoginRequiredMixin, TemplateView):
    """
    **InvoiceImportView(LoginRequiredMixin, TemplateView)**

    The class is used to import Xero invoices in Bankifi/Cashflow
    """
    template_name = "cashflow/invoice/invoice_import.html"

    def get_context_data(self, **kwargs):
        """
        **get_context_data(self, **kwargs)**

        Override the method to setup additional context data.
        """
        context = super(InvoiceImportView, self).get_context_data(**kwargs)

        if ON_HEROKU:
            # Create a Xero object that allows access to the API
            xero = get_xero(self.request)
            invoices = xero.invoices.filter(Status='AUTHORISED')
            add_contacts(xero)

            # Add invoices to xero and context
            context['invoices'] = invoices
            context['invoice_count'] = len(invoices)
            context['add_count'] = add_invoices(self.request.user, invoices, xero)
        else:
            context['invoices'] = []
            context['invoice_count'] = 0

        return context


class InvoiceGenerateView(LoginRequiredMixin, TemplateView):
    """
    **InvoiceGenerateView(LoginRequiredMixin, TemplateView)**

    The class is used to generate a random set of invoices.
    """
    template_name = "cashflow/invoice/invoice_generate.html"

    def get_context_data(self, **kwargs):
        """
        **get_context_data(self, **kwargs)**

        Override the method to setup additional context data.
        """
        context = super(InvoiceGenerateView, self).get_context_data(**kwargs)

        context['form'] = InvoiceGenerateForm()

        return context


    def post(self, request, *args, **kwargs):
        """
        **post(self, request, *args, **kwargs)**

        Override the method to route to the ***InvoiceGeneratedView***
        """
        form = InvoiceGenerateForm(request.POST)
        # check whether form is valid:
        if form.is_valid():
            # If valid generate a random number of invoices
            number = form.cleaned_data['number']
            # Clear old transactions and invoices first
            clear_invoices(request.user)
            clear_transactions(request.user)
            generate_invoices(request.user, number)
            url = reverse('cashflow:invoicelist')
            return HttpResponseRedirect(url + '?number={0}'.format(number))
        else:
            return render(request, self.template_name, {'form': InvoiceGenerateForm()})



class InvoiceGeneratedView(LoginRequiredMixin, TemplateView):
    """
    **InvoiceGeneratedView(LoginRequiredMixin, TemplateView)**

    The class is used to confirm to the user that the random invoices have been generated.
    """
    template_name = "cashflow/invoice/invoice_generated.html"

    def get_context_data(self, **kwargs):
        context = super(InvoiceGeneratedView, self).get_context_data(**kwargs)
        context['number'] = self.request.GET.get('number')

        return context

# === Invoice View Methods ===

def make_offer(user):
    """
    **make_offer()**

    The method calculates a loan offer against the positive value of future receivables.

    The loan offer will only be made if future receivables and available funds outweigh future payables.

    **Returns:**

    A tuple containing a loan message and offer amount
    """

    receivables = Invoice.invoice_obj.receivables(user)
    payables = Invoice.invoice_obj.payables(user)
    # Hard coded business and savings account for demo.
    bank = sum([x.balance(user) for x in Account.objects.filter(customer=user, account_number__in=['98765432', '87654321'])])
    required = payables - bank

    # Print this out for debugging purposes throughout demo phase
    infolog.info("Amount required via loan: [{0}]\nAmount of payables: [{1}]\nAmount total in bank: [{2}]".format(required, payables, bank))

    # New calculations
    offer_amt = required if receivables + bank > required else 0.0
    # offer_amt = receivables - payables - bank if receivables + bank > required else 0.0
    days_to_pay = Invoice.invoice_obj.days_to_pay(user)
    last_date = Invoice.invoice_obj.last_due(user)

    interest = 0.0

    offer_total = offer_amt + interest

    infolog.info("Receivables {}, Payables {}, Bank {}, Required {}, Offer {}".format(receivables, payables, bank, required, offer_amt))
    infolog.info("Days to pay {}, Last Date {}".format(days_to_pay, last_date))


    if last_date is None:
        return ("Sorry we can't make you an offer at this time.", 0.0)
    elif offer_amt > 0 and days_to_pay > 0:
        return ("Your last invoice is due on {4}. We can help with cashflow \
                    and offer you £{0:,} for {1} days.\n As a special introductory offer, interest would be £{2:,} and total to payback is £{3:,}."\
                    .format(int(offer_amt), days_to_pay, int(interest), int(offer_total), last_date.due.strftime("%d %B %Y")), offer_amt)
    elif offer_amt < 0:
        return ("No finance available at the moment, as your debts outweight your future credits.", 0.0)
    else:
        return ("Sorry you have no invoices currently due.", 0.0)



def add_invoices(user, invoices, xero):
    """
    **add_invoices(invoices, xero)**

    The methods add a list of invoices to the Bankifi database if not already present

    **Parameters:**

    ***invoices***: a list of Xero invoices.

    ***xero***: Xero connection object.

    ***Returns:***

    A count of the number of invoices added.
    """
    add_count = 0
    for invoice in invoices:
        if not Invoice.objects.filter(customer=user, number=invoice.get('InvoiceNumber',None)).exists():
            contact_id = invoice.get('Contact', '').get('ContactID', '')
            contact = xero.contacts.filter(ContactID=contact_id)[0]

            new_invoice = Invoice(  customer=user,
                                    invoice_type=Invoice.RECEIVABLE,
                                    number=invoice.get('InvoiceNumber',''),
                                    contact=add_contact(contact),
                                    raised=invoice.get('Date',date.today()),
                                    bank_account=Account.objects.first(),
                                    due=invoice.get('DueDate',date.today()),
                                    amount=invoice.get('AmountDue',0)
                                )
            if new_invoice:
                new_invoice.save()
                add_count += 1

    return add_count


def generate_invoices(user, number=5):
    """
    **generate_invoices(number=5)**

    The method generates a random set of Bankifi invoices.

    **Parameters:**

    ***number***: Number of invoices to generate. Defaults to 5 invoices

    **Returns:**

    A list of random invoices
    """
    return [generate_random_invoice(user) for x in range(0, number)]


def generate_random_invoice(user):
    """
    **generate_random_invoice()**

    The method generates a random invoice.

    **Returns:**

    A randomly generated invoice
    """
    # Get a random date upto 28 days in the past
    raised = random_date(28)
    # Randomly make a choice between a Payable or Receivable invoice
    invoice_type = choice([Invoice.PAYABLE, Invoice.RECEIVABLE])
    # Randomly make a choice between a Paid or Unpaid invoice
    status = choice([Invoice.PAID, Invoice.UNPAID])
    # Set due date 28 days into the future from raised date
    due = raised + timedelta(days=28)
    if status == Invoice.PAID:
        # Randomly set actual date bases on raised date for PAID invoices
        actual = random_date((date.today()-raised).days, date.today())
    else:
        actual = None
    # Create and save random invoice
    invoice = Invoice(
                    customer=user,
                    invoice_type=invoice_type,
                      contact=choice(Contact.objects.all()),
                      raised=raised,
                      due=due,
                      actual=actual,
                      amount=randrange(100, 10000),
                      status=status,
                      bank_account= Account.objects.filter(customer=user, account_number=PAYABLE_ACCOUNT).first() \
                                        if invoice_type == Invoice.PAYABLE else Account.objects.filter(customer=user, account_id=RECEIVABLE_ACCOUNT).first()
        )

    if invoice:
        invoice.save()

    return invoice
