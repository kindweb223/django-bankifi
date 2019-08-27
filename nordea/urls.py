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
from .views import IndexView

from .views import (
        ContactCreateView,
        ContactDeleteView,
        ContactDetailView, 
        ContactListView, 
        ContactUpdateView,
    )

from .views import (
        AccountCreateView,
        AccountDeleteView,
        AccountDetailView, 
        AccountListView, 
        AccountUpdateView,
        NordeaAccountView,
    )


from .views import (
        TransactionCreateView,
        TransactionDeleteView,
        TransactionDetailView, 
        TransactionListView, 
        TransactionUpdateView,
        NordeaTransactionView,
        NordeaBreakdownView,
    )


# === URL Mappings ===

# Map urls to views
urlpatterns = [
    url(r'^$', NordeaAccountView.as_view(), name='index'),
    url(r'^contact$', ContactListView.as_view(), name='contactlist'), # /Contact/search
    url(r'^contact/create/$', ContactCreateView.as_view(), name='contactcreate'),  # /Contact/create/
    url(r'^contact/(?P<pk>\d+)/delete/$', ContactDeleteView.as_view(), name='contactdelete'),  # /Contact/1/delete/
    url(r'^contact/(?P<pk>\d+)/$', ContactDetailView.as_view(), name='contactdetail'), # /Contact/1/
    url(r'^contact/(?P<pk>\d+)/update/$', ContactUpdateView.as_view(), name='contactupdate'), # /contact/1/update/
    url(r'^account$', AccountListView.as_view(), name='accountlist'), # /account/search
    url(r'^account/create/$', AccountCreateView.as_view(), name='accountcreate'),  # /account/create/
    url(r'^account/(?P<pk>\d+)/delete/$', AccountDeleteView.as_view(), name='accountdelete'),  # /account/1/delete/
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='accountdetail'), # /account/1/
    url(r'^account/(?P<pk>\d+)/update/$', AccountUpdateView.as_view(), name='accountupdate'), # /account/1/update/
    url(r'^transaction$', TransactionListView.as_view(), name='transactionlist'), # /transaction/search
    url(r'^transaction/create/$', TransactionCreateView.as_view(), name='transactioncreate'),  # /transaction/create/
    url(r'^transaction/(?P<pk>\d+)/delete/$', TransactionDeleteView.as_view(), name='transactiondelete'),  # /transaction/1/delete/
    url(r'^transaction/(?P<pk>\d+)/$', TransactionDetailView.as_view(), name='transactiondetail'), # /transaction/1/
    url(r'^transaction/(?P<pk>\d+)/update/$', TransactionUpdateView.as_view(), name='transactionupdate'), # /transaction/1/update/
    url(r'^nordea_accounts/$', NordeaAccountView.as_view(), name='nordea_accounts'),
    url(r'^nordea_transactions/(?P<pk>[\w\-]+)/$', NordeaTransactionView.as_view(), name='nordea_transactions'),
    url(r'^nordea_breakdown$', NordeaBreakdownView.as_view(), name='nordea_breakdown'),

]