# -*- coding: utf-8 -*-
import requests
import json
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def get_non_oauth(url_tail):
    url = settings.OBP_API_ROOT + url_tail
    r = requests.get(url)
    if r.status_code == requests.codes.ok:

        decoded_data = r.content.decode('utf-8')
        reply = json.loads(decoded_data)    
    else:
        reply = None
    return reply


class BanksView(LoginRequiredMixin, TemplateView):
    template_name = "bankinfo/banks.html"
    
    def get_context_data(self, **kwargs):
        context = super(BanksView, self).get_context_data(**kwargs)
        
        reply = get_non_oauth("/banks")
        context['banks'] = reply.get('banks') if reply else {}

        return context


class ProductsView(LoginRequiredMixin, TemplateView):
    template_name = "bankinfo/products.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        
        reply = get_non_oauth("/banks/{0}/products".format(self.kwargs['bid']))
        context['products'] = reply.get('products') if reply else {}
        context['bank_name'] = self.request.GET.get("short_name", None)

        return context


        





