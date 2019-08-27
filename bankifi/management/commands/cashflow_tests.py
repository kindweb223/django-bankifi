# Enable use of explicit relative imports
from __future__ import absolute_import

from random import choice, randrange
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from cashflow.models import Contact, Account, Invoice, Transaction

PAYABLE_ACCOUNT = '45674523'
RECEIVABLE_ACCOUNT = '51387801-7668-48b0-a276-e8cadc2d33de' 

class Command(BaseCommand):
	help = 'Generates test data'

	def handle(self, *args, **options):
		# Calculate Cashflow
		response = clear_invoices()
		response = generate_invoices(100)
		set_test(response)
		self.stdout.write('Successfully called make post with the following response: %s' % response)


def clear_invoices():
	for x in Invoice.objects.all():
		x.delete()



def generate_invoices(number=5):
	return [generate_random_invoice() for x in range(0, number)]


def generate_random_invoice():
	raised = random_date(28)
	invoice_type = choice([Invoice.PAYABLE, Invoice.RECEIVABLE])
	status = choice([Invoice.PAID, Invoice.UNPAID])
	due = raised + timedelta(days=28)
	if status == Invoice.PAID:
		actual = random_date((due-raised).days, due)
	else:
		actual = None

	invoice = Invoice(invoice_type=invoice_type,
					  contact=choice(Contact.objects.all()),
					  raised=raised,
					  due=due,
					  actual=actual,
					  amount=randrange(100, 10000),
					  status=status,
					  bank_account= Account.objects.get(account_number=PAYABLE_ACCOUNT) \
					  					if invoice_type == Invoice.PAYABLE else Account.objects.get(account_id=RECEIVABLE_ACCOUNT)
		)

	if invoice:
		invoice.save()

	return invoice


def random_date(numdays=0, base=datetime.today()):
	return choice([base - timedelta(days=x) for x in range(0, numdays)])
	

def set_test(invoices):
	paid = set()
	unpaid = set()
	payable = set()
	receivable = set()

	for i in invoices:
		paid.add(i) if i.status == Invoice.PAID else unpaid.add(i)
		payable.add(i) if i.invoice_type == Invoice.PAYABLE else receivable.add(i)

	print("There are {0} paid receivables".format(len(paid) & len(receivable)))
	print("There are {0} unpaid receivables".format(len(unpaid) & len(receivable)))
	print("There are {0} paid payables".format(len(paid) & len(payable)))
	print("There are {0} paid unpayables".format(len(unpaid) & len(payable)))
		
			
		


''' For each bank account calculate cashflow
'''
def cashflows():
	# Get a list of bank accounts
	accounts = Account.objects.all()
	all_checkpoints = {}
	for account in accounts:
		checkpoints = []
		invoices = Invoice.objects.filter(bank_account=account, status=Invoice.UNPAID).order_by('expected')
		balance = account.balance
		new_balance = balance
		negative_days = 0
		negative_amount = 0
		print("{0} {1} Current Balance {2}".format(account.name, account.account_number, account.balance))
		for invoice in invoices:
			new_balance += -invoice.amount if invoice.invoice_type == invoice.PAYABLE else invoice.amount
			checkpoints.append((invoice, account, new_balance))
		all_checkpoints[account.account_number] = checkpoints

	check_needs(all_checkpoints)

			# print("{0} {1} {2} {3} New Balance {4}".format(invoice.number, invoice.expected, invoice.invoice_type, invoice.amount, new_balance))

		# print("{0} {1}".format(account.name, account.account_number))
	

	# Fake apply the transactions to the bank accounts and show the balance impact over time
def check_needs(all_checkpoints):
	# Check each account and see if it needs financing
	for k, accs in all_checkpoints.items():
		for inv in accs:
			if inv[2] < 0:
				print(inv)
				if inv[1].sweep_account is not None:
					check_sweep(inv, all_checkpoints.get(inv[1].sweep_account))




# def check_sweep(inv, sweep_cp):
# 	print("Checking if a sweep is allowed")

# 	if inv[1].sweep_account.balance +  inv[2] => 0:
		
# 		print("Hooray you can sweep {0} {1}".format(inv[1].sweep_account.balance, inv[2] ))
# 		return True
# 	else:
# 		print("Sorry no sweep available")
# 		return False 


# def check_finance(invoice):

# 	finance_dict = {

# 	}
# 	return finance_dict


