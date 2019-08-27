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

class IndexView(LoginRequiredMixin, TemplateView):
    """
    **IndexView(LoginRequiredMixin, TemplateView)**

    View to display index/homepage and setup Xero credentials URL.
    """
    template_name = "cashflow/forecast/forecast.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if ON_HEROKU:
            # Login to Xero to generate credentials to access the authorization URL and override default URI
            credentials = get_xero_credentials(self.request, self.request.build_absolute_uri(reverse('cashflow:loggedin')))
            # Setup the authorization URL xero needs to ask the user to provide consent
            context['authorization_url'] = credentials.url

        return context

    def get(self, request, *args, **kwargs):
        if ON_HEROKU:
            # Login to Xero to generate credentials to access the authorization URL and override default URI
            credentials = get_xero_credentials(self.request, self.request.build_absolute_uri(reverse('cashflow:loggedin')))
            return HttpResponseRedirect(credentials.url)
        else:
            return super(IndexView, self).get(request, *args, **kwargs)



            


class AuthorizeView(LoginRequiredMixin, TemplateView):
    """
    **AuthorizeView(LoginRequiredMixin, TemplateView)**

    View to display successful login to Xero message.
    """
    template_name = "cashflow/setup/authorize.html"
