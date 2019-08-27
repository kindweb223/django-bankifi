
""" 
# Library of utility methods

Provides a library of generic methods re-used across the Cashflow Application (aka Bankifi demo).
"""
"""
**Available Methods**

1. ***due_date*** - Calculates the due date from today given a number of day from now as a parameter.
2. ***random_date*** - Provides a random date with a base date as an input and a number of days as 
the max date range value.
3. ***month_name*** - converts a month number to a full or abbreviated month name
4. ***month_lag_lead*** - returns a list of leading and lagging months by abbreviated or full name
5. ***month_lead*** - returns a list of leading months by abbreviated or full name
6. ***month_lag*** - returns a list of lagging months by abbreviated or full name
"""

# === Imports ===

# Import Python modules
import calendar
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from random import choice, randrange

# === Utility Methods ===

def due_date(days=28):
    """
    **due_date(days=28)**

    Calculates the due date from today given a number of days from now as a parameter.

    **Parameters:**
    
    ***days***: number of days to offset the due date into the future. Defaults to 28 days.

    **Returns:**

    The due date.
    """
    return date.today() + timedelta(days=days)  



def random_date(numdays=0, base=date.today()):
    """
    **random_date(numdays=0, base=datetime.today())**

    Provides a random date with a base date as an input and a number of days in the past to offset the date to.

    **Parameters:**
    
    ***numdays***: number of days in the past to offset to.
    
    ***base***: base date to offset from.

    **Returns:** 

    A random date from the date range.
    """
    return choice([base - timedelta(days=x) for x in range(0, numdays)]) if numdays else date.today()


def month_name(month_number, full=False):
    """
    **month_name(month_number, full=False)**

    Converts a month number to a full or abbreviated month name.

    **Parameters:**

    ***month_number***: month number.
    
    ***full***: True for full month name False for abbreviated name.
            Defaults to abbreviated name.

    **Returns:**

    A full or abbreviated month name.
    """
    if full:
        return calendar.month_name[month_number]
    else:
        return calendar.month_abbr[month_number]


def month_lag_lead(months=1, full=False):
    """
    **month_lag_lead(months=1, full=False)** 

    Provides a list of leading and lagging months names.

    For example if month today is April month_lag_lead(1) would return [Mar, Apr, May].

    **Parameters:**
    
    ***months***: number of months each side of this month to add to list.
    
    ***full***: True for full month name False for abbreviated name.
            Defaults to abbreviated name.

    **Returns:**
    
    A list of full or abbreviated month names.
    """
    month_now = [month_name(datetime.now().month, full)]
    return month_lag(months, full) + month_now + month_lead(months, full)


def month_lead(months=1, full=False):
    """
    **month_lead(months=1, full=False)**

    Provides a list of leading months names.

    For example if month today is April month_lead(1) would return [May].

    **Parameters:**

    ***months***: number of months beyond this month to add to list.

    ***full***: True for full month name False for abbreviated name. Defaults to abbreviated name.

    **Returns:** 

    A list of full or abbreviated month names
    """
    month_list = []
    for m in range(months):
        month = (datetime.now() + relativedelta(months=m+1)).month
        month_list.append(month_name(month, full))
    
    return month_list
        
    
def month_lag(months=1, full=False):
    """
    **month_lag(months=1, full=False)**
    Provides a list of lagging months names.

    For example if month today is April month_lag(1) would return [Mar].

    **Parameters:**

    ***months***: number of months before this month to add to list.
    
    ***full***: True for full month name False for abbreviated name. Defaults to abbreviated name.

    **Returns:**

    A list of full or abbreviated month names
    """
    month_list = []
    for m in range(months):
        month = (datetime.now() - relativedelta(months=m+1)).month
        month_list.append(month_name(month, full))

    return month_list

    