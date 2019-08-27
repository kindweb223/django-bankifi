
""" Django Application URL to view mappings for Demo APIs """

# Import Django modules
from django.conf.urls import url, include
from django.contrib.auth.models import User
# Import django-rest-framework-swagger modules

from rest_framework import routers, serializers, viewsets
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_swagger.views import get_swagger_view

# Import views
from .views import (
        ContactViewSet,
        AccountViewSet,
        TransactionViewSet,
        NetworthAPIView,
        CreditsAPIView,
        DebitsAPIView,
        # ContactListAPIView,
        # ContactCreateAPIView,
        # ContactDetailAPIView,
        # # InvoiceListAPIView,
        # # InvoiceCreateAPIView,
        # # InvoiceDetailAPIView,
        # AccountListAPIView,
        # AccountCreateAPIView,
        # AccountDetailAPIView,
        # TransactionListAPIView,
        # TransactionCreateAPIView,
        # TransactionDetailAPIView,
        ForecastAPIView,
    )

# Setup routers and set trailing_slash=False for this to work with WSO2
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'contacts', ContactViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)

# router.register(r'contact', ContactListAPIView)
# router.register(r'contact/create', ContactCreateAPIView)
# router.register(r'contact/(?P<pk>[0-9]+)/', ContactDetailAPIView)
# # router.register(r'invoice', InvoiceListAPIView,)
# # router.register(r'invoice/create', InvoiceCreateAPIView)
# # router.register(r'invoice/(?P<pk>[0-9]+)/', InvoiceDetailAPIView)
# router.register(r'account', AccountListAPIView)
# router.register(r'account/create', AccountCreateAPIView)
# router.register(r'account/(?P<pk>[0-9]+)/', AccountDetailAPIView)
# router.register(r'transaction', TransactionListAPIView,)
# router.register(r'transaction/create', TransactionCreateAPIView)
# router.register(r'transaction/(?P<pk>[0-9]+)/', TransactionDetailAPIView)
# router.register(r'forecast', ForecastAPIView,)

# Setup Swagger schema (requires testing)
# schema_view = get_swagger_view(title='Bankifi API')
schema_view = get_schema_view(title='Bankifi Nordea API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# Map API urls to views
urlpatterns = [
    url(r'^$', schema_view, name="docs"),
    url(r'^', include(router.urls)),

    # url(r'^contact$', ContactListAPIView.as_view(), name='contactlist'), # /api/contact
    # url(r'^contact/create$', ContactCreateAPIView.as_view(), name='contactcreate'), # /api/cashflow/contact
    # url(r'^contact/(?P<pk>[0-9]+)/$', ContactDetailAPIView.as_view(), name='contactdetail'), # /api/casflow/contact/{}

    # url(r'^account$', AccountListAPIView.as_view(), name='accountlist'), # /api/cashflow/account
    # url(r'^account/create$', AccountCreateAPIView.as_view(), name='accountcreate'), # /api/cashflow/account/create
    # url(r'^account/(?P<pk>[0-9]+)/$', AccountDetailAPIView.as_view(), name='accountdetail'), # /api/casflow/account/{}/delete

    # url(r'^transaction$', TransactionListAPIView.as_view(), name='transactionlist'), # /api/cashflow/transaction
    # url(r'^transaction/create$', TransactionCreateAPIView.as_view(), name='transactioncreate'), # /api/cashflow/transaction/create
    # url(r'^transaction/(?P<pk>[0-9]+)/$', TransactionDetailAPIView.as_view(), name='transactiondetail'), # /api/casflow/transaction/{}/delete

    url(r'^forecast/(?P<pk>[\w\-]+)/$', ForecastAPIView.as_view(), name='forecast'), # /api/cashflow/forecast
    url(r'^networth$', NetworthAPIView.as_view(), name='networth'), # /api/aggregate/grouptotal/1/?base=EUR
    url(r'^credits$', CreditsAPIView.as_view(), name='credits'), # /api/aggregate/grouptotal/1/?base=EUR
    url(r'^debits$', DebitsAPIView.as_view(), name='debits'), # /api/aggregate/grouptotal/1/?base=EUR
]