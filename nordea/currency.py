from django.db.models import Case, When, FloatField, Sum, F
from aggregate.models import Group
from cashflow.models import Account, Transaction

from django.contrib.humanize.templatetags.humanize import intcomma

from aggregate.helpers import get_rates
from nordea.breakdown import get_breakdown


breakdown = get_breakdown()


def total_networth(base='EUR'):
    # rates = get_rates(base)
    # total = breakdown.get('total',0.0)/rates['EUR']
    total = 200.50
    return intcomma(round(total,2))


def total_credits(base='EUR'):
    # rates = get_rates(base)
    # total = breakdown.get('credits',0.0)/rates['EUR']
    total = 100.50
    return intcomma(round(total,2))


def total_debits(base='EUR'):
    # rates = get_rates(base)
    # total = breakdown.get('debits',0.0)/rates['EUR']
    total = 30.50
    return intcomma(round(total,2))


    