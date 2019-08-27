''' Provides transaction breakdown '''

import json
import pandas as pd
import numpy as np
import datetime
from calendar import month_name

from nordea.helpers import nordea_api

def get_transactions(pk):
    ''' Calls Nordea to receive the transactions '''
    context = {}
    url_tail = "/accounts/{0}/transactions".format(pk)
    r = nordea_api(url_tail)
    if r.get('content', None) is not None:
        transactions = r.get('content', None)['response']['transactions']
        context['transactions'] = transactions
        context['account'] = r.get('content', None)['response']['account']

    return context

def parse_float(x):
    ''' Parses a float string and returns a float '''
    try:
        x = float(x)
    except Exception:
        x = 0
    return x


def parse_date(d):
    ''' Parses a date string and returns datetime '''
    date = datetime.datetime.strptime(d, "%Y-%m-%d")

    return date


def get_breakdown(pk="FI6593857450293470-EUR"):
    ''' Provides a breakdown of transaction details '''
    trans_list = []
    # Prepare transactions for data frame
    trans_raw = get_transactions(pk)
    if 'transactions' in trans_raw:
        for t in trans_raw:
            record = []
            record.append(t['bookingDate']['date'])
            record.append(t['creditDebitIndicator'])
            record.append(float(t['amount']['value']) if t['creditDebitIndicator'] == "CRDT"
                          else float(t['amount']['value']) * -1)
            trans_list.append(record)

    # Create Data frames and calculations
    stops = pd.DataFrame(trans_list, columns=['date', 'indicator', 'amount'])
    stops["date"] = stops['date'].apply(parse_date)
    # txpmth = stops["date"].dt.month.value_counts()
    stops = stops.set_index('date')
    debits = stops[stops['indicator'] == "DBIT"]
    credits = stops[stops['indicator'] == "CRDT"]

    # total = pd.concat([debits,credits])

    # Prepare dictionary of values to return
    reply_dict = {}
    debitsum = debits['amount'].sum()
    creditsum = credits['amount'].sum()
    reply_dict['debits'] = debitsum
    reply_dict['credits'] = creditsum
    reply_dict['total'] = debitsum + creditsum
    # reply_dict['max_credit'] = credits["amount"].max()
    # reply_dict['min_credit'] = credits["amount"].min()
    # reply_dict['min_mean'] = round(credits["amount"].mean(),2)
    # reply_dict['max_debit'] = debits["amount"].min()
    # reply_dict['min_debit'] = debits["amount"].max()
    # reply_dict['mean_debit'] = round(debits["amount"].mean(),2)
    # reply_dict['month_trans'] = txpmth.to_dict()
    # reply_dict['month_debit'] = debits.groupby(debits.index.month)['amount'].sum()
    # reply_dict['month_credit'] = credits.groupby(credits.index.month)['amount'].sum()
    # reply_dict['month_total'] = total.groupby(total.index.month)['amount'].sum()
    # reply_dict['debitsum'] = get_month_totals(reply_dict.get('month_debit'))
    # reply_dict['creditsum'] = get_month_totals(reply_dict.get('month_credit'))
    # reply_dict['totalsum'] = get_month_totals(reply_dict.get('month_total'))

    return reply_dict


def get_month_totals(thedict):
    months = []
    totals = []
    back = []
    border = []
    for key, value in thedict.items():
        months.append(month_name[key])
        totals.append(round(value,2))
        back.append('rgba(1, 1, 1, 0.2)' if value >= 0 else 'rgba(255,99,132,0.2)',)
        border.append('rgba(1, 1, 1, 1)' if value >= 0 else 'rgba(255,99,132,1)',)

    reply_dict = {}
    reply_dict["months"] = months
    reply_dict["totals"] = totals
    reply_dict["back"] = back
    reply_dict["border"] = border

    return reply_dict
