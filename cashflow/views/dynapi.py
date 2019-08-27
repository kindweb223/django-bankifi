"""
# Views for Index

Django Views for Index (Demo Home Page)
"""
""" 
**View Classes:**

1. ***IndexView***: View to display index/homepage and setup Xero credentials URL.
2. ***AuthorizeView***: View to display successful login to Xero message.
"""

# === Imports ===

# Import Python modules
from os import environ
import requests
import json

# Import Django modules
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

# Import Xero oauth module
from utility.xeroutil import get_xero_credentials, get_xero

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')

# === Classes ===

class DynapiView(LoginRequiredMixin, TemplateView):
    """
    **IndexView(LoginRequiredMixin, TemplateView)**

    View to display index/homepage and setup Xero credentials URL.
    """
    template_name = "cashflow/dynapi.html"

    def get_context_data(self, **kwargs):
        context = super(DynapiView, self).get_context_data(**kwargs)
        if ON_HEROKU:
            # Login to Xero to generate credentials to access the authorization URL and override default URI
            credentials = get_xero_credentials(self.request, self.request.build_absolute_uri(reverse('cashflow:loggedin')))
            # Setup the authorization URL xero needs to ask the user to provide consent
            context['authorization_url'] = credentials.url
        else:
            context['authorization_url'] = "http://sandbox.marketplace.motivelabs.com:8101/xero/oauth/authorize?profile=Bankifi"

        # Some Tests To Dynapi
        # url = "http://sandbox.marketplace.motivelabs.com:8101/xero/oauth/authorize?profile=Axone"

        # r = requests.get(url)
        # if r.status_code == requests.codes.ok:
        #     decoded_data = r.content.decode('utf-8')
        #     data = json.loads(decoded_data) 
        #     print(data)
        # else:
        #     print("Dynapi failed with error {0}".format)

        return context
            


