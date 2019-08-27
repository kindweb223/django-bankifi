# -*- coding: utf-8 -*-
import requests
import json
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin



def get_oauth(request):
    openbank = OAuth1Session(
        settings.OAUTH_CLIENT_KEY,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        resource_owner_key=request.session['oauth_token'],
        resource_owner_secret=request.session['oauth_secret']
    )
    return openbank


def get_non_oauth(url_tail):
    url = settings.OBP_API_ROOT + url_tail
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        reply = json.loads(r.content)
    else:
        reply = None
    return reply


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "obp_oauth/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        openbank = OAuth1Session(
            settings.OAUTH_CLIENT_KEY,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            callback_uri=settings.OAUTH_CALLBACK_URI
        )

        fetch_response = openbank.fetch_request_token(settings.OAUTH_TOKEN_URL)
        authorization_url = openbank.authorization_url(settings.OAUTH_AUTHORIZATION_URL)

        self.request.session['oauth_token'] = fetch_response.get('oauth_token')
        self.request.session['oauth_secret'] = fetch_response.get('oauth_token_secret')
        self.request.session.modified = True

        context['authorization_url'] = authorization_url
        return context


class AuthorizationView(LoginRequiredMixin, TemplateView):
    template_name = "obp_oauth/authorization.html"

    def get_context_data(self, **kwargs):
        context = super(AuthorizationView, self).get_context_data(**kwargs)

        openbank = OAuth1Session(
            settings.OAUTH_CLIENT_KEY,
            client_secret=settings.OAUTH_CLIENT_SECRET,
            resource_owner_key=self.request.session['oauth_token'],
            resource_owner_secret=self.request.session['oauth_secret']
        )

        openbank.parse_authorization_response(self.request.build_absolute_uri())

        fetch_response = openbank.fetch_access_token(settings.OAUTH_ACCESS_TOKEN_URL)


        self.request.session['oauth_token'] = fetch_response.get('oauth_token')
        self.request.session['oauth_secret'] = fetch_response.get('oauth_token_secret')

        context['private_bank_json'] = fetch_response
        return context

'''
Provides a list of customer accounts and detailed information across banks
'''
class BankView(LoginRequiredMixin, TemplateView):
    template_name = "obp_oauth/view_accounts.html"

    def get_context_data(self, **kwargs):
        context = super(BankView, self).get_context_data(**kwargs)

        openbank = get_oauth(self.request)

        # Need to call this API to get list of current user accounts
        url =  settings.OBP_API_ROOT + "/accounts/public"

        accounts = openbank.get(url).json()

        account_list = []
        for account in accounts:
            # Call get_account_by_id to get balance and other info using bank_id and account id
            url = settings.OBP_API_ROOT + "/my/banks/{0}/accounts/{1}/account".format(account.get('bank_id'), account.get('id'))
            details = openbank.get(url).json()

            # Some of the accounts are not accessible so we filter them out
            if details.get('error', None) is None:
                account_list.append(details)

        context['accounts'] = account_list

        return context











