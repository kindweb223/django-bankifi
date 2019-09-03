"""
#Forecast Views

Django Views for Forecast
"""
"""
**View Classes:**

1. ***ForecastView***: View to display the Invoice and Bank Account Cashflow.

**Internal Methods:**

1. ***cashflows***: Returns a list of invoice checkpoints and bank balances .
2. ***check_sweep***: Checks if a sweep is possible against and account and withdrawal amount.
3. ***schedule***: Produces a schedule of invoice payments, actionable insights and account balances.
"""

# === Imports ===

# Import Django modules
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Import Bankifi/Cashflow Models
from cashflow.models import Account, Invoice, Loan

# Import application utility methods
from cashflow.utilities import month_lag_lead

# === Globals ===

# Hard coded Xero receivable account to be used
RECEIVABLE_ACCOUNT = '8b5367e1-7fb5-4810-9f69-ddb2b26b68a4'


# === Classes ===

class ForecastView(LoginRequiredMixin, TemplateView):
    """
    **ForecastView(LoginRequiredMixin, TemplateView)**

    View to display the Invoice and Bank Account Cashflow
    """
    template_name = "cashflow/forecast/forecast.html"

    def get_context_data(self, *args, **kwargs):
        # Setup the context data to return to the view
        context = super(ForecastView, self).get_context_data(*args, **kwargs)
        context['all_checkpoints'] = cashflows(self.request.user)
        context['accounts'] = Account.objects.filter(customer=self.request.user)
        context['best'] = schedule(self.request.user, False)
        account = Account.objects.filter(account_id=RECEIVABLE_ACCOUNT).first()
        loan = Loan.objects.filter(customer=self.request.user, status=Loan.OUTSTANDING).first()
        context['balance'] = "{0:,}".format(account.balance(self.request.user) if account else 0.0)
        context['loan'] = "{0:,}".format(loan.balance if loan else 0.0)
        context['sweep_acc'] = account.sweep_account.account_number if account and account.sweep_account else ''
        context['sweep_name'] = account.sweep_account.name if account and account.sweep_account else ''
        context['sweep_bal'] = "{0:,}".format(account.sweep_account.balance(self.request.user) if account and account.sweep_account else 0.0)
        context['worse'] = schedule(self.request.user)
        context['payables'] = "{0:,}".format(Invoice.invoice_obj.payables(self.request.user))
        context['receivables'] = "{0:,}".format(Invoice.invoice_obj.receivables(self.request.user))
        context['pay_lables'] = month_lag_lead(1)
        # Setup messages from payment and loan screens
        context['title'] = self.request.session.get('title', '')
        context['description'] = self.request.session.get('description', '')
        context['status'] = self.request.session.get('status', '')
        # Reset session after
        self.request.session['title'] = ''
        self.request.session['description'] = ''
        self.request.session['status'] =  ''

        amount = float(self.request.GET.get('offer_amount', '0').translate({ord(c): None for c in ' ,'}))
        account = self.request.GET.get('account', '')
        context['offer_amount'] = amount
        context['account'] = account

        return context

# === Methods ===

def cashflows(user):
    """
    **cashflows()**

    Returns a dictionary of invoice checkpoints and bank balances.

    **Returns:**

    A dictionary keyed on bank account number associated list of invoice checkpoints and associated bank balances.
    """
    # Get a list of bank accounts
    accounts = Account.objects.filter(customer=user)
    all_checkpoints = {}
    for account in accounts:
        checkpoints = []
        invoices = Invoice.objects.filter(customer=user, bank_account=account, status=Invoice.UNPAID).order_by('expected')
        balance = account.balance(user)
        new_balance = balance
        negative_days = 0
        negative_amount = 0

        for invoice in invoices:
            new_balance += -invoice.amount if invoice.invoice_type == invoice.PAYABLE else invoice.amount
            checkpoints.append((invoice, account, new_balance, check_sweep(user, account, new_balance)))
        all_checkpoints[account.account_number] = checkpoints

    return all_checkpoints


def check_sweep(user, account, amount):
    """
    **check_sweep(account, amount)**

    Checks if a sweep is possible against and account and withdrawal amount.

    **Parameters:**

    ***account***: Account to check if sweep is available from.

    ***amount***: amount required.

    **Returns:**

    True if sweep is available or False if sweep is unavailable.
    """
    if amount < 0 and account.sweep_account and account.sweep_account.balance(user) +  amount >= 0:
        return True
    else:
        return False



def schedule(user, worsecase=True):
    """
    **schedule(worsecase=True)**

    Schedules a forecast of cashflows and actionable insights.

    **Parameters:**

    ***worsecase***: True if due dates (worse case) are to be used or False if expected dates (best case).

    **Returns:**
    A list of entries containing payment date, amount, bank account balance,
    sweep balance and recommended actionable actions.
    """
    if worsecase:
        invoices = Invoice.objects.filter(customer=user, status=Invoice.UNPAID).order_by('due')
    else:
        invoices = Invoice.objects.filter(customer=user, status=Invoice.UNPAID).order_by('expected')

    account = Account.objects.filter(customer=user, account_id=RECEIVABLE_ACCOUNT).first()
    if account is not None:
        bank = account.balance(user)
    else:
        bank = 0.0
    if account is not None and account.sweep_account is not None:
        sweep = account.sweep_account.balance(user)
    else:
        sweep = 0.0
    loan_account = Loan.objects.filter(customer=user).first()
    if loan_account is not None:
        loan = loan_account.balance
    else:
        loan = 0.0

    payamount = 0.0
    recamount = 0.0
    current_date = None
    options = []
    schedule_list = []

    for i in invoices:
        thedate = i.due if worsecase == True else i.expected
        if current_date is None:
            current_date = thedate

        if thedate != current_date:
            options = []
            netamount = recamount - payamount
            bank += netamount

            recamount = payamount = 0.0
            if loan > 0.0 and bank > loan:
                options.append("Pay off £{0:,} loan".format(loan))
                bank -= loan
                loan = 0.0
            if bank < 0.0 and sweep > 0:
                required = -bank
                available = required if sweep > required else sweep
                bank += available
                sweep -= available
                options.append("Sweep £{0:,} from savings".format(available))
            elif bank < 0.0 and bank >= -1000:
                options.append("Go overdrawn £{0:,}".format(bank))
            elif bank < 0.0:
                required = -bank
                loan += required
                bank += required
                options.append("Borrow{1} £{0:,}".format(required, ' additional' if loan else ''))

            schedule_list.append([current_date, "{0:,}".format(netamount), "{0:,}".format(bank), "{0:,}".format(sweep), "{0:,}".format(loan), ". ".join(options)])
            netamount = 0.0
            current_date = thedate
        if i.invoice_type == Invoice.RECEIVABLE:
            recamount += i.amount
        else:
            payamount += i.amount

    if invoices.exists():
        # Handle last iteration
        netamount = recamount - payamount
        bank += netamount
        recamount = payamount = 0.
        options = []
        if loan > 0.0 and bank > loan:
            options.append("Pay off £{0:,} loan".format(loan))
            bank -= loan
            loan = 0.0
        if bank < 0.0 and sweep > 0:
            required = -bank
            available = required if sweep > required else sweep
            bank += available
            sweep -= available
            options.append("Sweep £{0:,} from savings".format(available))
        elif bank < 0.0 and bank >= -1000:
            options.append("Go overdrawn £{0:,}".format(bank))
        elif bank < 0.0:
            required = -bank
            loan += required
            bank += required
            options.append("Borrow{1} £{0:,}".format(required, ' additional' if loan else ''))


        schedule_list.append([current_date, "{0:,}".format(netamount), "{0:,}".format(bank),  "{0:,}".format(sweep), "{0:,}".format(loan), ". ".join(options)])
        netamount = 0.0

    return schedule_list
