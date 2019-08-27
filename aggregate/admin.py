from django.contrib import admin

from django.conf import settings
from django.contrib.auth.models import User


# Register your models here.
from .models import Group,  Consent
# from .models import Group, Account, Transaction, Consent
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'title')
    # exclude = ('customer',)
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "customer":
    #         kwargs["queryset"] = User.objects.all().order_by('email')
    #     return super(GroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "accounts":
            kwargs["queryset"] = Account.objects.filter(customer=request.user).order_by('name')
        return super(GroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.customer = request.user
        obj.save()


# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'bank', 'name', 'sortcode', 'account_number', 'currency')
#     # exclude = ('customer',)
    
#     def save_model(self, request, obj, form, change):
#         obj.customer = request.user
#         obj.save()
#     # def formfield_for_foreignkey(self, db_field, request, **kwargs):
#     #     if db_field.name == "customer":
#     #         kwargs["queryset"] = User.objects.all().order_by('email')
#     #     return super(AccountAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# class TransactionAdmin(admin.ModelAdmin):
#     """
#     **TransactionAdmin(admin.ModelAdmin)**

#     Admin class for Transaction Model.
#     """
#     list_display = ('id', 'customer', 'created', 'account', 'transaction_type', 'description', 'amount')
#     # list_editable = ('account', 'transaction_type', 'description', 'amount')
#     # search_fields = ['account']

#     def save_model(self, request, obj, form, change):
#         obj.customer = request.user
#         obj.save()
    

class ConsentAdmin(admin.ModelAdmin):
    """
    **TransactionAdmin(admin.ModelAdmin)**

    Admin class for Transaction Model.
    """
    list_display = ('id', 'customer', 'created', 'account')
    # list_editable = ('account', 'transaction_type', 'description', 'amount')
    # search_fields = ['account']

    def save_model(self, request, obj, form, change):
        obj.customer = request.user
        obj.save()
    

admin.site.register(Group, GroupAdmin)
# admin.site.register(Account, AccountAdmin)
# admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Consent, ConsentAdmin)



