from django.db.models import Case, When, FloatField, Sum, F
from django.contrib.humanize.templatetags.humanize import intcomma

from cashflow.models import Account, Transaction

from aggregate.models import Group
from aggregate.helpers import get_rates


def total_group_balance(customer, base='EUR'):
    ''' Get the total balance of all customers groups in a particular currency '''
    rates = get_rates(base)

    groups = Group.objects.filter(customer=customer).\
                annotate(gbp=Case(
                    When(accounts__currency=Account.GBP, then=Sum(F('accounts__transaction__amount')/rates['GBP'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(eur=Case(
                    When(accounts__currency=Account.EURO, then=Sum(F('accounts__transaction__amount')/rates['EUR'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(usd=Case(
                    When(accounts__currency=Account.USD, then=Sum(F('accounts__transaction__amount')/rates['USD'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(total=F('gbp') + F('eur') + F('usd'))
    total = 0.0
    for e in groups:
        total += e.total if e.total is not None else 0.0

    return intcomma(round(total,2))


# def total_account_balance(pk=1, base='EUR'):
#     ''' Get the total balance of all customers groups in a particular currency '''
#     rates = get_currency(['EUR', 'GBP', 'USD'], base)

#     accounts = Account.objects.filter(customer__pk=pk).\
#                 annotate(gbp=Case(
#                     When(currency=Account.GBP, then=Sum(F('transaction__amount')/rates['GBP'])),
#                     default=0, output_field=FloatField(),
#                 )).\
#                 annotate(eur=Case(
#                     When(currency=Account.EURO, then=Sum(F('transaction__amount')/rates['EUR'])),
#                     default=0, output_field=FloatField(),
#                 )).\
#                 annotate(usd=Case(
#                     When(currency=Account.USD, then=Sum(F('transaction__amount')/rates['USD'])),
#                     default=0, output_field=FloatField(),
#                 )).\
#                 annotate(total=F('gbp') + F('eur') + F('usd'))
#     total = 0.0    
#     for e in accounts:
#         total += e.total if e.total else 0.0
    
#     return intcomma(round(total,2))


def total_account_balance(customer, base='EUR'):
    return transaction_total({'customer': customer, 'account__consent__isnull': False}, base)


def total_networth(customer, base='EUR'):
    return transaction_total({'customer': customer, 'account__consent__isnull': False}, base)


def total_credits(customer, base='EUR'):
    return transaction_total({'customer': customer, 'account__consent__isnull': False, 'transaction_type': Transaction.CREDIT}, base)


def total_debits(customer, base='EUR'):
    return transaction_total({'customer': customer, 'account__consent__isnull': False, 'transaction_type': Transaction.DEBIT}, base)


def transaction_total(rules, base):
    ''' Get the total networth in a particular currency '''
    rates = get_rates(base)

    transactions = Transaction.objects.filter(**rules).\
                annotate(gbp=Case(
                    When(currency=Transaction.GBP, then=Sum(F('amount')/rates['GBP'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(eur=Case(
                    When(currency=Transaction.EURO, then=Sum(F('amount')/rates['EUR'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(usd=Case(
                    When(currency=Transaction.USD, then=Sum(F('amount')/rates['USD'])),
                    default=0, output_field=FloatField(),
                )).\
                annotate(total=F('gbp') + F('eur') + F('usd'))
    total = 0.0    
    for e in transactions:
        total += e.total if e.total else 0.0

    return intcomma(round(total,2))





    