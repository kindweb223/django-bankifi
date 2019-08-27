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
from .views import IndexView,  CustomerView, CustomerAccountView, AccountView, TransactionView, BreakdownView

# === URL Mappings ===

# Map urls to views
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^customers/$', CustomerView.as_view(), name='customers'),
    url(r'^accounts/$', AccountView.as_view(), name='accounts'),
    url(r'^accounts/(?P<pk>[\w\-]+)/$', AccountView.as_view(), name='accounts'),
    url(r'^customeraccounts/(?P<pk>[\w\-]+)/$', CustomerAccountView.as_view(), name='customeraccounts'),
    url(r'^transactions/(?P<pk>[\w\-]+)/$', TransactionView.as_view(), name='transactions'),
    url(r'^breakdown/(?P<pk>[\w\-]+)/$', BreakdownView.as_view(), name='breakdown'),
]