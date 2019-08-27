
from calendar import month_name
import itertools

from django.db import models
from django.db.models import F, When, Case
from django.db.models import Sum, Avg, FloatField
from django.db.models.functions import ExtractMonth
from django.utils import timezone

from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# from aggregate.helpers import get_rates




class Base(models.Model):
    """
    **Base(models.Model)**

    Base parent model for all the models to provide a set of standard timestamp methods.

    **Public Attributes:**

    ***timestamp***: Editable timestamp.

    ***created***: Date and time model instance was created.

    ***updated***: Date and time model instance was updated.
    """
    timestamp = models.DateTimeField(blank=True, editable=False, db_index=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, editable=False, verbose_name="Last Updated")

    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    # Override save method.
    def save(self,  *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()

        update_timestamp = kwargs.pop('update_timestamp', False)
        if update_timestamp:
            self.timestamp = timezone.now()

        super(Base, self).save(*args, **kwargs)



# class Account(Base):
#     """
#     **Account(Base)**

#     A representation of a Bank Account.

#     """
    
#     # Subset of available banks. Add to this list to add more or setup in database in future.
#     BARCLAYS = 'Barclays'
#     BBVA = 'BBVA'
#     HSBC = 'HSBC'
#     LLOYDS = 'Lloyds'
#     NATIONWIDE = 'Nationwide'
#     NORDEA = 'Nordea'
#     RBS = 'RBS'
#     SANTANDER = 'Santander'

#     BANK = (
#         (BARCLAYS, 'Barclays'),
#         (BBVA, 'BBVA'),
#         (HSBC, 'HSBC'),
#         (LLOYDS, 'Lloyds'),
#         (NATIONWIDE, 'Nationwide'),
#         (NORDEA, 'Nordea'),
#         (RBS, 'RBS'),
#         (SANTANDER, 'Santander'),
#     )

#     EURO = 'EURO'
#     USD = 'USD'
#     GBP = 'GBP'

#     CURRENCY = (
#         (EURO, 'EURO'),
#         (USD, 'USD'),
#         (GBP, 'GBP'),
#     )
#     customer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, 
#         verbose_name="Customer")
#     bank = models.CharField(choices=BANK, max_length=10, help_text="Bank", 
#         verbose_name="Bank", default=NATIONWIDE)
#     name = models.CharField(max_length=40, 
#         verbose_name="Account Name", blank=True)
#     sortcode = models.CharField(max_length=11, validators=[MinLengthValidator(6)], 
#         verbose_name="Sort Code/Swift BIC", blank=True)
#     account_number = models.CharField(max_length=20, 
#         validators=[MinLengthValidator(8)], verbose_name="Account Number/IBAN")
#     currency = models.CharField(choices=CURRENCY, max_length=10, help_text="Currency", 
#         verbose_name="Currency", default=EURO)

#     sweep_min_balance = models.FloatField(default=0, 
#         verbose_name="Sweep Balance Limit")
#     sweep_account = models.ForeignKey('Account', null=True, blank=True,
#         verbose_name="Sweep Account")

#     # Override save method to setup made up bank sortcodes and conduct account sweep if necessary.
#     def save(self,  *args, **kwargs):
#         sort_codes = {
#             'BARCLAYS': '111111',
#             'HSBC': '222222',
#             'NORDEA': '333333',
#             'NATIONWIDE': '444444',
#             'RBS': '555555',
#             'LLOYDS': '666666',
#             'SANTANDER': '777777',
#             'BBVA': '888888',
#         }
#         super(Account, self).save(*args, **kwargs)

#         if not self.name:
#             self.name = "Bank Account {0}".format(self.id)
#             # Save to set primary key id
#             super(Account, self).save(*args, **kwargs)

#         if not self.sortcode:
#             self.sortcode = sort_codes.get(self.bank, '000000')
#             super(Account, self).save(*args, **kwargs)

#         if self.balance < self.sweep_min_balance:
#             self.sweep()

        
#     def sweep(self, amount=0.0):
#         """
#         **sweep(self, amount=0.0)**

#         Sweep funds from linked bank account to restore balance to minimum level.

#         Sweeps only the funds required to make withdrawal amount and set account to minimum balance.

#         **Parameters:**

#         ***amount***: amount to be withdrawn from account.

#         **Returns:**

#         Nothing
#         """
#         amount_required = (amount - self.balance) + self.sweep_min_balance
#         if self.sweep_account:
#             # If the withdrawal is successful then make the deposit for the sweep
#             if self.sweep_account.withdraw(amount_required, "Sweep Payment to {0} {1}".format(self.sortcode, self.account_number)):
#                 self.deposit(amount_required, "Sweep Payment from {0} {1}".format(self.sortcode, self.account_number))
            
            

#     def deposit(self, amount=0.0, description="Deposit"):
#         """
#         **deposit(self, amount=0.0, description="Deposit", xero=None, contact_id=None, account_id='')**

#         Deposit funds into bank account.

#         **Parameters:**

#         ***amount***: deposit amount.

#         ***description***: deposit description.

#         **Returns:**

#         True if successful. False if unsuccessful.
#         """
#         # Only deposit positive amounts > 0
#         if amount > 0:
#             # Create bankif transaction to deposit funds
#             t = Transaction(account=self, customer=self.customer, transaction_type=Transaction.CREDIT, amount=amount, 
#                     currency=self.currency, description=description)
            
#             # Save Bankifi Transaction
#             if t is not None:
#                 t.save()
#             return True
#         else:
#             return False


#     def withdraw(self, amount=0.0, description="Withdrawal"):
#         """
#         **withdraw(self, amount=0.0, description="Withdrawal")**

#         Withdraw funds from bank account. 

#         **Parameters:**

#         ***amount***: withdrawal amount.

#         ***description***: withdrawal description.

#         **Returns:**

#         True is successful. False if unsuccessful.
#         """
#         # Check the withdrawal amount is > 0 and that the account has sufficient funds for withdrawal
#         if amount > 0 and self.transaction_check(amount):
#             # Create bankif transaction to withdraw funds
#             t = Transaction(account=self, customer=self.customer, transaction_type=Transaction.DEBIT, amount=amount, 
#                     currency=self.currency, description=description)
            
#             # Save Bankifi Transaction
#             if t is not None:
#                 t.save()
#             return True
#         else:
#             return False


#     def transaction_check(self, amount):
#         """
#         **transaction_check(self, amount)**

#         Checks account has sufficient funds prior to making withdrawal.

#         Will include the funds available within a sweep account as part of the check if necessary.


#         **Parameters:**

#         ***amount***: withdrawal amount

#         **Returns:**

#         True if successful. False if unsuccessful.
#         """
#         if self.balance >= amount:
#             return True
#         elif self.sweep_account and self.sweep_account.transaction_check(amount-self.balance):
#             self.sweep(amount)
#             return True
#         else:
#             return False 


#     @property
#     def balance(self):
#         """
#         **balance(self)**

#         Returns the balance of the bank account.

#         Aggregates the transactions against the account to find the current balance.

#         **Returns:**

#         The account balance or 0 if no transactions exist.
#         """     
#         if Transaction.objects.filter(account_id=self.id).exists():
#             return Transaction.objects.filter(account_id=self.id).aggregate(Sum('amount')).get('amount__sum',0.0)
#         else:
#             return 0.0


#     def get_absolute_url(self):
#         return reverse("aggregate:accountdetail", kwargs={"pk":self.pk})

#     def __str__(self):     
#         return "{} {}".format(self.bank, self.name)
        

#     class meta:
#         ordering = ['bank',]


# class TransactionManager(models.Manager):
#     """
#     **TransactionManager(models.Manager)**

#     Provides a number of aggregation methods for the Transaction Class.

#     **Methods:**

#     1. ***networth*** - Returns the networth of the individual.
#     2. ***debits*** - Returns the total value of debits across accounts.
#     3. ***credit*** - Returns the total valie of credits across accounts.
   
#     """
#     def networth(self, customer, base):
#         """
#         **networth(self)**

#         Returns the total networth of the account balances.

#         **Returns:**

#         The networth.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """
#         months, totals = self.trans_stats({'customer': customer, 'amount__isnull': False}, base)

#         return {'months': months, 'networths': totals}


#     def networth_total(self, customer):
#         """
#         **debit_total(self)**

#         Returns the total value of all debits across accounts.

#         **Returns:**

#         The total networth across accounts.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """
#         # Using the database to do all the work using aggregation
#         total = Transaction.objects.filter(customer=customer, amount__isnull=False).\
#                                 aggregate(networth=Sum('amount')).get('networth', 0.0)

#         return total



#     def credits(self, customer, base):
#         """
#         **credits(self)**

#         Returns the total value of all credits across accounts.

#         **Returns:**

#         The total credits.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """

#         months, totals = self.trans_stats({'customer': customer, 'amount__isnull': False, 
#                         'transaction_type': Transaction.CREDIT}, base)
        
#         return {'months': months, 'credits': totals}


#     def credit_total(self, customer):
#         """
#         **credit_total(self)**

#         Returns the total value of all credits across accounts.

#         **Returns:**

#         The total credits.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """
#         # Using the database to do all the work using aggregation
#         total = Transaction.objects.filter(customer=customer, amount__isnull=False, transaction_type=Transaction.CREDIT).\
#                                 aggregate(credits=Sum('amount')).get('credits', 0.0)

#         return total


#     def debits(self, customer, base):
#         """
#         **debits(self)**

#         Returns the total value of all debits across accounts.

#         **Returns:**

#         The total debits.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """

#         months, totals = self.trans_stats({'customer': customer, 'amount__isnull': False, 
#                         'transaction_type': Transaction.DEBIT}, base)
        
#         return {'months': months, 'debits': totals}



#     def debit_total(self, customer):
#         """
#         **debit_total(self)**

#         Returns the total value of all debits across accounts.

#         **Returns:**

#         The total debits.

#         TODO: At the moment we just total the amount and do no currency conversion. This needs to be done.
#         """
#         # Using the database to do all the work using aggregation
#         total = Transaction.objects.filter(customer=customer, amount__isnull=False, transaction_type=Transaction.DEBIT).\
#                                 aggregate(debits=Sum('amount')).get('debits', 0.0)

#         return total


#     def trans_stats(self, rules, base):
#         # rates = get_rates(base)

#         # transactions = Transaction.objects.filter(**rules).\
#         #         annotate(period=ExtractMonth('transdate')).values('period').\
#         #         annotate(gbp=Case(
#         #             When(currency=Transaction.GBP, then=Sum(F('amount')/rates['GBP'])),
#         #             default=0, output_field=FloatField(),
#         #         )).\
#         #         annotate(eur=Case(
#         #             When(currency=Transaction.EURO, then=Sum(F('amount')/rates['EUR'])),
#         #             default=0, output_field=FloatField(),
#         #         )).\
#         #         annotate(usd=Case(
#         #             When(currency=Transaction.USD, then=Sum(F('amount')/rates['USD'])),
#         #             default=0, output_field=FloatField(),
#         #         )).\
#         #         annotate(total=F('gbp') + F('eur') + F('usd')).\
#         #         order_by('period')

#         months = []
#         totals = []
#         # for key, group in itertools.groupby(transactions, lambda item: item["period"]):
#         #     months.append(month_name[key])
#         #     total = sum([item["total"] for item in group])
#         #     totals.append(round(total, 2))

#         return months, totals


# class Transaction(Base):
#     """
#     **Transaction(Base)**

#     A representation of a bank transaction.

#     A transaction can be a debit or a credit transaction.

#     **Public Attributes:**

#     ***account***: foreign key to bank account.

#     ***account***: foreign key to customer.

#     ***transaction_type***: type of transaction; DEBIT or CREDIT.

#     ***amount***: transaction amount.

#     ***transdate***: date and time of transaction.

#     """
#     DEBIT = 'DEBIT'
#     CREDIT = 'CREDIT'
#     TRANSACTION_TYPE = (
#         (DEBIT, 'Debit'),
#         (CREDIT, 'Credit'),
#     )

#     EURO = 'EURO'
#     USD = 'USD'
#     GBP = 'GBP'

#     CURRENCY = (
#         (EURO, 'EURO'),
#         (USD, 'USD'),
#         (GBP, 'GBP'),
#     )

#     account = models.ForeignKey('Account', help_text="Bank Account", verbose_name="Account", on_delete=models.CASCADE)
#     customer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, 
#         verbose_name="Customer", help_text="Customer")
#     transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=10, help_text="Transaction type", 
#         verbose_name="Type")
#     currency = models.CharField(choices=CURRENCY, max_length=10, help_text="Currency", 
#         verbose_name="Currency", default=EURO)
#     amount = models.FloatField(default=0.0, help_text="Transaction Amount", verbose_name="Amount")
#     description = models.CharField(max_length=250, help_text="Transaction description", verbose_name="Description", 
#         blank=True)
#     transdate = models.DateTimeField(blank=True, verbose_name="Date and Time", help_text="Transaction date and time", 
#         auto_now=True)

#     objects = TransactionManager()

#     class meta:
#         ordering = ['-created']


#     # Override save method to ensure correct amounts are applied to the account.
#     def save(self,  *args, **kwargs):
#         if not self.description:
#             self.description = "{0} Payment".format(self.transaction_type)

#         # Ensure positive amounts from credits and negative amount for debits
#         if self.amount < 0.0 and self.transaction_type == self.CREDIT:
#             self.amount = self.amount * -1.0

#         if self.amount > 0.0 and self.transaction_type == self.DEBIT:
#             self.amount = self.amount * -1.0

#         self.currency = self.account.currency

#         super(Transaction, self).save(*args, **kwargs)

#         if self.account.balance < self.account.sweep_min_balance:
#             self.account.sweep()
        

#     def __str__(self):
#         return "{0}".format(self.id)


#     def get_absolute_url(self):
#         return reverse("aggregate:transactiondetail", kwargs={"pk":self.pk})



class Group(Base):
    title = models.CharField(max_length=30)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, 
        verbose_name="Customer", help_text="Customer")
    # accounts = models.ManyToManyField(Account)
    accounts = models.ManyToManyField('cashflow.Account')

    def get_absolute_url(self):
        return reverse("aggregate:groupdetail", kwargs={"pk":self.pk})

    def __str__(self):     
        return self.title

    class Meta:
        ordering = ('title',)



class Consent(Base):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, 
        verbose_name="Customer", help_text="Customer")
    account = models.ForeignKey('cashflow.Account', help_text="Bank Account", verbose_name="Account", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("aggregate:consentdetail", kwargs={"pk":self.pk})

    def __str__(self):     
        return "{} {}".format(self.account.bank, self.account.account_number)

    class Meta:
        ordering = ('account',)

    