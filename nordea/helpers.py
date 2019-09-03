# Import Python modules
from os import environ
import requests
import json
from requests_oauthlib import OAuth1Session

from django.conf import settings


# OATH STUFF

def nordea_oauth():
    ''' Use Nordea OAUTH API. Returns hardcoded 'authenticated-user-full-access' token
        # import requests
        # >>> headers = {}
        # >>> headers['X-IBM-Client-Secret'] = 'saerw4RAWEfwq4ir240jriw40jar2304jra4'
        # >>> headers['X-IBM-Client-Id'] = 'ababababab-fefe-fafa-b3b3-111112a11111'
        # >>> headers['Content-Type'] = 'application/json'
        # >>> r = requests.post(NORDEA_API_ROOT + '/v1/authentication/access_token?code=user-full-access', headers=headers)
        # >>> r.status_code
        # 200
        # >>> r.text
        # '{"access_token":"authenticated-user-full-access","expires_in":830,"token_type":"BEARER"}'
    '''
    headers = {}
    headers['X-IBM-Client-Id'] = 'f5548266-7053-4f5a-b376-3e5ab8dc0f8a'
    headers['X-IBM-Client-Secret'] = 'yS5eM8hF1uT2sT4yG0hF8pR2kB3lT4kO0tA8kU3sE5eT7bD3uB'
    headers['Content-Type'] = 'application/json'

    auth_url = settings.NORDEA_API_ROOT + '/v1/authentication/access_token?code=user-full-access'

    return requests.post(auth_url, headers=headers)


def nordea_api(url_tail):
    # headers = {}
    # headers['Authorization'] = 'Bearer authenticated-user-full-access'
    # headers['X-IBM-Client-Id'] = 'f5548266-7053-4f5a-b376-3e5ab8dc0f8a'
    # headers['X-IBM-Client-Secret'] = 'yS5eM8hF1uT2sT4yG0hF8pR2kB3lT4kO0tA8kU3sE5eT7bD3uB'
    # headers['Content-Type'] = 'application/json'
    # url = settings.NORDEA_API_ROOT + url_tail

    # r =  requests.get(url, headers=headers)

    reply_dict = {}
    # if r.status_code == requests.codes.ok:
    #     reply_dict['content'] = json.loads(r.content)
    # else:
    #     reply_dict['content'] = None
    #     reply_dict['error'] = json.loads(r.content).get('error', "").get('failures', "")[0]
    return reply_dict


def get_currency(values):
    ''' Returns currencies relative to the EURO

        Parameters: pass in a comma seperate list of currency codes (i.e GB,USD)
        Returns a dictionary with the values for each item

        http://api.fixer.io/latest?symbols=USD,GBP
        {
            "base": "EUR",
            "date": "2017-06-28",
            "rates": {
                "GBP": 0.88525,
                "USD": 1.1375
            }
        }

    '''
    url = "http://api.fixer.io/latest?symbols=" + ",".join(values)

    r = requests.get(url)
    reply_dict = {}
    if r.status_code == requests.codes.ok:
        content = json.loads(r.content)
        for v in values:
            reply_dict[v] = content.get('rates', "").get(v, 0)
    # else:
    #     reply_dict['content'] = None
        # reply_dict['error'] = json.loads(r.content).get('error', "").get('failures', "")[0]

    return reply_dict
