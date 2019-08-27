""" 
# URL to view mappings 

Django allows us to map urls to Django view functions or classes. 

This file provides the URL mappings to the Cashflow application (aka Bankifi demo) views.
"""

# === Imports ===

# Import django modules
from django.conf.urls import url
from django.views.generic.base import RedirectView

# Import views
from .views.forecast import ForecastView
from .views.index import IndexView, AuthorizeView
from .views.setup import SetupView, LoggedInView
from .views.pobo import PoboCreateView, PoboPayView, PoboPaymentView, PoboThankyouView

from .views.dynapi import DynapiView

from .views.loan import (
        LoanApplyView,
        LoanThankyouView, 
        LoanPayView,
    )

from .views.contact import (
        ContactCreateView,
        ContactDeleteView,
        ContactDetailView, 
        ContactListView, 
        ContactUpdateView,
        ContactImportView, 
    )

from .views.account import (
        AccountCreateView,
        AccountDeleteView,
        AccountDetailView, 
        AccountListView, 
        AccountUpdateView,
        AccountImportView, 
    )


from .views.transaction import (
        TransactionCreateView,
        TransactionDeleteView,
        TransactionDetailView, 
        TransactionListView, 
        TransactionUpdateView,
        TransactionImportView, 
    )

from .views.invoice import (
        InvoiceCreateView,
        InvoiceDeleteView,
        InvoiceDetailView, 
        InvoiceListView, 
        InvoiceUpdateView,
        InvoiceImportView,
        InvoiceGenerateView,
        InvoiceGeneratedView,
    )

# === URL Mappings ===

# Map urls to views
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^contact/import$', ContactImportView.as_view(), name='contactimport'),
    url(r'^contact$', ContactListView.as_view(), name='contactlist'), # /Contact/search
    url(r'^contact/create/$', ContactCreateView.as_view(), name='contactcreate'),  # /Contact/create/
    url(r'^contact/(?P<pk>\d+)/delete/$', ContactDeleteView.as_view(), name='contactdelete'),  # /Contact/1/delete/
    url(r'^contact/(?P<pk>\d+)/$', ContactDetailView.as_view(), name='contactdetail'), # /Contact/1/
    url(r'^contact/(?P<pk>\d+)/update/$', ContactUpdateView.as_view(), name='contactupdate'), # /contact/1/update/

    url(r'^invoice/import$', InvoiceImportView.as_view(), name='invoiceimport'),
    url(r'^invoice$', InvoiceListView.as_view(), name='invoicelist'), # /invoice/search
    url(r'^invoice/create/$', InvoiceCreateView.as_view(), name='invoicecreate'),  # /invoice/create/
    url(r'^invoice/(?P<pk>\d+)/delete/$', InvoiceDeleteView.as_view(), name='invoicedelete'),  # /invoice/1/delete/
    url(r'^invoice/(?P<pk>\d+)/$', InvoiceDetailView.as_view(), name='invoicedetail'), # /invoice/1/
    url(r'^invoice/(?P<pk>\d+)/update/$', InvoiceUpdateView.as_view(), name='invoiceupdate'), # /invoice/1/update/
    url(r'^invoice/generate$', InvoiceGenerateView.as_view(), name='invoicegenerate'),  # /invoice/generate/

    url(r'^account/import$', AccountImportView.as_view(), name='accountimport'),
    url(r'^account$', AccountListView.as_view(), name='accountlist'), # /account/search
    url(r'^account/create/$', AccountCreateView.as_view(), name='accountcreate'),  # /account/create/
    url(r'^account/(?P<pk>\d+)/delete/$', AccountDeleteView.as_view(), name='accountdelete'),  # /account/1/delete/
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='accountdetail'), # /account/1/
    url(r'^account/(?P<pk>\d+)/update/$', AccountUpdateView.as_view(), name='accountupdate'), # /account/1/update/
    url(r'^invoice/generate$', InvoiceGenerateView.as_view(), name='invoicegenerate'),  # /invoice/generate/
    url(r'^invoice/generated$', InvoiceGeneratedView.as_view(), name='invoicegenerated'),  # /invoice/generated/

    url(r'^transaction/import$', TransactionImportView.as_view(), name='transactionimport'),
    url(r'^transaction$', TransactionListView.as_view(), name='transactionlist'), # /transaction/search
    url(r'^transaction/create/$', TransactionCreateView.as_view(), name='transactioncreate'),  # /transaction/create/
    url(r'^transaction/(?P<pk>\d+)/delete/$', TransactionDeleteView.as_view(), name='transactiondelete'),  # /transaction/1/delete/
    url(r'^transaction/(?P<pk>\d+)/$', TransactionDetailView.as_view(), name='transactiondetail'), # /transaction/1/
    url(r'^transaction/(?P<pk>\d+)/update/$', TransactionUpdateView.as_view(), name='transactionupdate'), # /transaction/1/update/

    url(r'^forecast$', ForecastView.as_view(), name='forecast'), # /transaction/search

    url(r'^loanapply/$', LoanApplyView.as_view(), name='loanapply'),
    url(r'^loanpay/$', LoanPayView.as_view(), name='loanpay'),
    url(r'^loanthankyou/$', LoanThankyouView.as_view(), name='loanthankyou'),

    url(r'^setup$', SetupView.as_view(), name='setup'),
    url(r'^loggedin$', LoggedInView.as_view(), name='loggedin'),


    url(r'^authorize$', AuthorizeView.as_view(), name='authorize'),
    url(r'^dynapi$', DynapiView.as_view(), name='dynapi'),

    url(r'^pobo/create$', PoboCreateView.as_view(), name='pobocreate'),
    url(r'^pobo/pay$', PoboPayView.as_view(), name='pobopay'),
    url(r'^pobo/payment$', PoboPaymentView.as_view(), name='pobopayment'),
    url(r'^pobo/thankyou$', PoboThankyouView.as_view(), name='pobothankyou'),
]