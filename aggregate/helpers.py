# Import Python modules
from os import environ
import requests
import json
from requests_oauthlib import OAuth1Session

from django.conf import settings
from django.core.cache import cache


def get_currency(symbols, base='EUR'):
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
    url = "http://api.fixer.io/latest?base={0}&symbols={1}".format(base, ",".join(symbols))

    r = requests.get(url)
    reply_dict = {}
    if r.status_code == requests.codes.ok:
        content = json.loads(r.content)
        for v in symbols:
            reply_dict[v] = content.get('rates', "").get(v, 0) if v.upper() != base.upper() else 1
    
    return reply_dict


def get_rates(base):
    currencies = cache.get(base)
    if currencies is None:
        currencies = get_currency(['EUR', 'GBP', 'USD'], base)
        cache.set(base, currencies, 300)
    return currencies