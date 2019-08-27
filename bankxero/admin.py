from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Loan, BankAccount

class LoanModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'balance')
	class Meta:
		model = Loan
            

class BankAccountModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'balance')
	class Meta:
		model = BankAccount

admin.site.register(Loan, LoanModelAdmin)
admin.site.register(BankAccount, BankAccountModelAdmin)