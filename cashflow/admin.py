""" 
# Django admin entries 

The Django admin provides a ready to use set of forms to maintain the application database. 
It allows databases tables to be viewed, added to, updated, rows to be deleted, etc. 
Access to the admin is via [admin url](demo.bankifi.com/admin).
"""
"""
**Admin classes:**

1. ***ContactAdmin*** - Admin class for Contact Model.
2. ***InvoiceAdmin*** - Admin class for Invoice Model.
3. ***AccountAdmin*** - Admin class for Account Model.
4. ***TransactionAdmin*** - Admin class for Transaction Model.
5. ***LoanAdmin*** - Admin class for Loan Model.
"""

# === Imports ===

# Import Django modules
from django.contrib import admin

# Import Bankifi/Cashflow models
from .models import (
			Contact, 
			Invoice, 
			Account, 
			Transaction,
            Loan,
		)


# === Admin Classes ===

class ContactAdmin(admin.ModelAdmin):
    """
    **ContactAdmin(admin.ModelAdmin)**

    Admin class for Contact Model.
    """
    list_display = ('id', 'name', 'first_name', 'last_name', 
        'timestamp', 'created', 'updated')
    list_editable = ('name', 'first_name', 'last_name')
    search_fields = ['name']



class InvoiceAdmin(admin.ModelAdmin):
    """
    **InvoiceAdmin(admin.ModelAdmin)**

    Admin class for Invoice Model
    """
    list_display = ('id', 'customer', 'invoice_type', 'number', 'contact', 'raised', 'due', 
        'expected', 'planned', 'actual', 'status', 'bank_account', 'amount')
    list_editable = ('invoice_type', 'number', 'contact', 'raised', 'due', 'expected', 'planned', 
        'actual', 'status',  'bank_account', 'amount')
    search_fields = ['number']



class AccountAdmin(admin.ModelAdmin):
    """
    **AccountAdmin(admin.ModelAdmin)**

    Admin class for Account Model.
    """
    list_display = ('id', 'customer', 'bank', 'name', 'sortcode', 'account_number', 'currency', 'sweep_account', 
        'sweep_min_balance')
    list_editable = ('bank', 'name', 'account_number')
    search_fields = ['name', 'account_number', 'bank', 'sort_code']

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "sweep_account":
    #         kwargs["queryset"] = Account.objects.filter(customer=request.user).order_by('name')
    #     return super(AccountAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def save_model(self, request, obj, form, change):
    #     obj.customer = request.user
    #     obj.save()


class TransactionAdmin(admin.ModelAdmin):
    """
    **TransactionAdmin(admin.ModelAdmin)**

    Admin class for Transaction Model.
    """
    list_display = ('id', 'customer', 'created', 'account', 'transaction_type', 'description', 'currency', 'amount')
    list_editable = ('account', 'transaction_type', 'description', 'amount')
    search_fields = ['account']

    # def save_model(self, request, obj, form, change):
    #     obj.customer = request.user
    #     obj.save()



class LoanAdmin(admin.ModelAdmin):
    """
    **LoanAdmin(admin.ModelAdmin)**

    Admin class for Loan Model.
    """
    list_display = ('id', 'balance', 'account', 'status')
    list_editable = ('account',)
    search_fields = ['account']

# === Admin Registration ===
    
# Register classes with Django Admin
admin.site.register(Contact, ContactAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Loan, LoanAdmin)