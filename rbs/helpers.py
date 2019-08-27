# Import Python modules
from os import environ
import requests
import json
from requests_oauthlib import OAuth1Session

from django.conf import settings


# OATH STUFF

def bank_oauth():
    ''' Use OAUTH API. Need to adapt on a per bank basis
    '''
    headers = {}
    headers['X-IBM-Client-Id'] = 'f5548266-7053-4f5a-b376-3e5ab8dc0f8a'
    headers['X-IBM-Client-Secret'] = 'yS5eM8hF1uT2sT4yG0hF8pR2kB3lT4kO0tA8kU3sE5eT7bD3uB'
    headers['Content-Type'] = 'application/json'


 # https://login.microsoftonline.com/bluebankb2c.onmicrosoft.com/oauth2/v2.0/authorize?
 #    p=B2C_1_BlueBankSUSI&client_Id=0f7ef810-2f9c-424c-942a-48c6ea361d9a&nonce=defaultNonce&redirect_uri=https%3A%2F%2Flocalhost%3A44316%2F.auth%2Flogin%2Faad%2Fcallback&scope=openid&response_type=id_token&prompt=login

    auth_url = settings.NORDEA_API_ROOT + '/v1/authentication/access_token?code=user-full-access'
    return requests.post(auth_url, headers=headers)


def bank_api(url_tail):
    ''' Handles the banks API request. Override if necessary for each bank.
    '''
    headers = {}
    headers['Ocp-Apim-Subscription-Key'] = settings.RBS_PRIMARY_SUB_KEY
    headers['Authorization'] = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJleHAiOjE0OTk0MjIxNzgsIm5iZiI6MTQ5OTQxODU3OCwidmVyIjoiMS4wIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5taWNyb3NvZnRvbmxpbmUuY29tL2Q1Zjg1NjgyLWY2N2EtNDQ0NC05MzY5LTJjNWVjMWEwZThjZC92Mi4wLyIsInN1YiI6ImE2OTk3NWM3LTNmNmUtNGE4MC04ZWUxLTQyNzA1ZmVlMTU4ZSIsImF1ZCI6IjQwOTU3YjljLTYzYmMtNGFiNC05ZWNiLTY3YjU0M2M4ZTRjYSIsIm5vbmNlIjoiZGVmYXVsdE5vbmNlIiwiaWF0IjoxNDk5NDE4NTc4LCJhdXRoX3RpbWUiOjE0OTk0MTg1NzgsIm9pZCI6ImE2OTk3NWM3LTNmNmUtNGE4MC04ZWUxLTQyNzA1ZmVlMTU4ZSIsIm5hbWUiOiJLZW5ueSIsImZhbWlseV9uYW1lIjoiTWFycml0dCIsImdpdmVuX25hbWUiOiJLZW5ldGgiLCJlbWFpbHMiOlsia2VubmV0aC5tYXJyaXR0QG1lLmNvbSJdLCJ0ZnAiOiJCMkNfMV9CbHVlQmFua1NVU0kifQ.fXOdf_oNWdb5u0rwHep7zX8XYyWYM3Dk9-b2JmxvAw11BFdOKHas48xhZwSx7Z-SmsxtRzGPf8frV1z_B4tQIfGWnYJExv682qHEfvKlEwP1MWys3NyzCKAtstIqJKLlR2Lkitju5siOVTmNAorvv23yvpdkjgeM2FC04nprQcItTWi-oKD8YRwVJfKGgVc_v1hqUExL6Rk84CgWCTT3w4O81Wmu7rJH_lndhmBG-ejN6iglSIiXfXzb9j_SKeJYI8yXo_4bfGDB-V_fXgdHK3B7IU2zTQqGiCfqwJ02ym891-wc5lO8hoQSjBE_YKTk43kVrjnGsbZI8r3OwBReDQ'
    # headers['X-IBM-Client-Id'] = 'f5548266-7053-4f5a-b376-3e5ab8dc0f8a'
    # headers['X-IBM-Client-Secret'] = 'yS5eM8hF1uT2sT4yG0hF8pR2kB3lT4kO0tA8kU3sE5eT7bD3uB'
    # headers['Content-Type'] = 'application/json'
    url = settings.RBS_API_ROOT + url_tail

    print(url)
    r =  requests.get(url, headers=headers)

    reply_dict = {}
    if r.status_code == requests.codes.ok:
        reply_dict['content'] = json.loads(r.content)
    else:
        reply_dict['content'] = None
        reply_dict['error'] = json.loads(r.content)

    print(reply_dict)
    return reply_dict


def get_currency(values):
    ''' Returns currencies relative to the EURO from fixer.io

        Parameters: pass in a comma seperate list of currency codes (i.e GB,USD)
        Returns a dictionary with the values for each item
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
