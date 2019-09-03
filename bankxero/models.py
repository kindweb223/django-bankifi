from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Loan(models.Model):
	balance = models.FloatField(default=0, verbose_name="Loan Balance")

	def pay_loan():
		self.balance = 0.0

	def __str__(self):
		return "{0}".format(self.balance)


# Create your models here.
class BankAccount(models.Model):
	balance = models.FloatField(default=0, verbose_name="Account Balance")

	def __str__(self):
		return "{0}".format(self.balance)

