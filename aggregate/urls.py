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
from .views import IndexView, CreateUserView, AccountSetupView, ManageConsentView, AccountDashboardView

from .views import (
        AccountCreateView,
        AccountDeleteView,
        AccountDetailView, 
        AccountListView, 
        AccountAddView, 
        AccountUpdateView,
        AccountTransactionListView,
    )

from .views import (
        GroupCreateView,
        GroupDeleteView,
        GroupDetailView, 
        GroupListView, 
        GroupUpdateView,
        GroupTransactionListView,
    )


from .views import (
        ConsentCreateView,
        ConsentDeleteView,
        ConsentDetailView,
        ConsentListView,
        AuthoriseView,
        AuthenticateView,
    )


from .views import (
        TransactionCreateView,
        TransactionDeleteView,
        TransactionDetailView, 
        TransactionListView, 
        TransactionUpdateView,
    )


# === URL Mappings ===

# Map urls to views
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # url(r'^dashboard$', IndexView.as_view(), name='dashboard'),


    url(r'^createuser$', CreateUserView.as_view(), name='createuser'),
    url(r'^accountsetup$', AccountSetupView.as_view(), name='accountsetup'),
    url(r'^manageconsent$', ManageConsentView.as_view(), name='manageconsent'),
    url(r'^dashboard$', AccountDashboardView.as_view(), name='accountdashboard'),

    url(r'^account$', AccountListView.as_view(), name='accountlist'), # /account/search
    url(r'^account/create/$', AccountCreateView.as_view(), name='accountcreate'),  # /account/create/
    url(r'^account/(?P<pk>\d+)/delete/$', AccountDeleteView.as_view(), name='accountdelete'),  # /account/1/delete/
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='accountdetail'), # /account/1/
    url(r'^account/(?P<pk>\d+)/update/$', AccountUpdateView.as_view(), name='accountupdate'), # /account/1/update/
    url(r'^groupacctrans/(?P<pk>\d+)/$', AccountTransactionListView.as_view(), name='accounttransactionlist'), # /transaction/search
    url(r'^account/add/$', AccountAddView.as_view(), name='accountadd'), # /account/search

    url(r'^group$', GroupListView.as_view(), name='grouplist'), # /group/search
    url(r'^group/create/$', GroupCreateView.as_view(), name='groupcreate'),  # /group/create/
    url(r'^group/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groupdelete'),  # /group/1/delete/
    url(r'^group/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='groupdetail'), # /group/1/
    url(r'^group/(?P<pk>\d+)/update/$', GroupUpdateView.as_view(), name='groupupdate'), # /account/1/update/
    url(r'^grouptrans/(?P<pk>\d+)/$', GroupTransactionListView.as_view(), name='grouptransactionlist'), # /transaction/search
    
    url(r'^transaction$', TransactionListView.as_view(), name='transactionlist'), # /transaction/search
    url(r'^transaction/create/$', TransactionCreateView.as_view(), name='transactioncreate'),  # /transaction/create/
    url(r'^transaction/(?P<pk>\d+)/delete/$', TransactionDeleteView.as_view(), name='transactiondelete'),  # /transaction/1/delete/
    url(r'^transaction/(?P<pk>\d+)/$', TransactionDetailView.as_view(), name='transactiondetail'), # /transaction/1/
    url(r'^transaction/(?P<pk>\d+)/update/$', TransactionUpdateView.as_view(), name='transactionupdate'), # /transaction/1/update/

    url(r'^consent$', ConsentListView.as_view(), name='consentlist'), # /consent
    url(r'^consent/create/$', ConsentCreateView.as_view(), name='consentcreate'),  # /consent/create/
    url(r'^consent/(?P<pk>\d+)/delete/$', ConsentDeleteView.as_view(), name='consentdelete'),  # /consent/1/delete/
    url(r'^consent/(?P<pk>\d+)/$', ConsentDetailView.as_view(), name='consentdetail'), # /consent/1/
    url(r'^consent/authenticate/$', AuthenticateView.as_view(), name='authenticate'), # /consent
    url(r'^consent/authorise/$', AuthoriseView.as_view(), name='authorise'), # /consent

]

 