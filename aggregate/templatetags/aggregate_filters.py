""" 
#Library template filters 

Template filters are used to provide additional functionality within Django's templates.
These methods are used by the Cashflow (aka Bankifi Demo) project templates.
"""
"""
**Available functions:**

1. ***get_dict_item***: Returns an item from a dictionary using provided key.
2. ***get_item***: Returns an item from a list using provided key(index).
3. ***month_name***: Converts a month number to a month name.
"""

# === Imports ===

import calendar

from django import template

from cashflow.models import Account

register = template.Library()

# === Methods ===

@register.filter
def get_dict_item(thedict, key):
    """
    **get_dict_item(thedict, key)**

    Returns an item from a dictionary using provided key.

    **Parameters:**

    ***thedict***: the dictionary.

    ***key***: key to use to return dictionary item.

    **Returns**:

    The item from the dictionary or an empty string.
    """
    if thedict:
        return thedict.get(key)
    else:
        ""


@register.filter
def get_item(thelist, key):
    """
    **get_item(thelist, key)**

    Returns an item from a list using a provided key(index).

    **Parameters:**

    ***thelist***: the list.

    ***key***: key/index to use to return list item.

    **Returns**:

    The item from the list or an empty string.
    """
    return thelist[key] if thelist and key < len(thelist) else ""


@register.filter
def month_name(month_number):
    """
    **month_name(month_number)**

    Converts a month number to a full month name.

    **Parameters**:

    ***month_number***: month number.

    **Return**:

    Full month name.
    """
    return calendar.month_name[month_number]


@register.filter
def fx(amount, rate):
    """
    **fx(source, rate)**

    Applies a currency rate to the amount to calculate exchange value

    **Parameters**:

    ***amount***: amount to be used.
    ***rate***: exchange rate to be applied.

    **Return**:

    Converted amount.
    """
    return round(float(amount) * float(rate), 2) if amount and rate else 0.0


@register.filter
def currency(currency_type):
    """
    **currency(currency_type)**

    Converts a currency type to the symbol to be used

    **Parameters**:

    ***currency_type***: type of currency

    **Return**:

    Currency symbol.
    """
    if currency_type == Account.USD:
        return '$'
    elif currency_type == Account.EURO:
        return '€'
    elif currency_type == Account.GBP:
        return '£'
    else:
        return ''
    
