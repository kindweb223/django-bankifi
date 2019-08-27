"""
# Contact Views

Django Views for Contact Model
"""
""" 
**View Classes:**

1. ***ContactCreateView***: View to create a contact.
2. ***ContactDeleteView***: View to delete a contact.
3. ***ContactDetailView***: View to provide a contacts details.
4. ***ContactListView***: View to provide a list of contacts.
5. ***ContactUpdateView***: View to update an contact.
6. ***ContactImportView***: View to import contacts from Xero.

**Internal Methods:**

1. ***add_contacts***: Add all contacts to Bankifi imported from Xero.
2. ***add_contact***: Add a contact to Bankifi imported from Xero.
"""

# === Imports ===

# Import Python modules
from os import environ

# Import Django modules
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Import Bankifi/Cashflow Models
from cashflow.models import Contact

# Import Bankifi/Cashflow View/Form models and methods
from django.views.generic import (
	    DetailView, 
	    ListView, 
	    CreateView, 
	    UpdateView, 
	    DeleteView,
        TemplateView,
    )

from cashflow.forms import ContactModelForm

# Import Xero oauth module
from utility.xeroutil import get_xero

# === Globals ===

# Environment variable used for local and production testing
ON_HEROKU = environ.get('ON_HEROKU')


# === Classes ===

class ContactCreateView(LoginRequiredMixin, CreateView):
    """
    **ContactCreateView(LoginRequiredMixin, CreateView)**

    View to create a Bankifi/Cashflow contact.
    """ 
    template_name = "cashflow/contact/contact_create.html"
    form_class = ContactModelForm
    success_url = reverse_lazy("cashflow:contactlist")



class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """
    **ContactDeleteView(LoginRequiredMixin, DeleteView)**

    View to delete a Bankifi/Cashflow contact.
    """ 
    template_name = "cashflow/contact/contact_confirm_delete.html"
    model = Contact
    success_url = reverse_lazy("cashflow:contactlist")



class ContactDetailView(LoginRequiredMixin, DetailView):
    """
    **ContactDetailView(LoginRequiredMixin, DetailView)**

    View to view details of a Bankifi/Cashflow contact.
    """ 
    template_name = "cashflow/contact/contact_detail.html"
    queryset = Contact.objects.all()



class ContactListView(LoginRequiredMixin, ListView):
    """
    **ContactListView(LoginRequiredMixin, ListView)**

    View to display list of Bankifi/Cashflow contacts.
    """ 
    template_name = "cashflow/contact/contact_list.html"
    # Allows search to be added
    def get_queryset(self, *args, **kwargs):
        qs = Contact.objects.all()    
            
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(ContactListView, self).get_context_data(*args, **kwargs)
        context['authorization_url'] = reverse_lazy("cashflow:contactimport")
        # Add URL shortcuts to allow create, update and delete from list view
        context['create_url'] = reverse_lazy(':contactcreate')
        context['update_url'] = reverse_lazy(':contactupdate')
        context['delete_url'] = reverse_lazy(':contactdelete')
        return context



class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """
    **ContactUpdateView(LoginRequiredMixin, UpdateView)**

    View to update a Bankifi/Cashflow contact.
    """ 
    template_name = "cashflow/contact/contact_update.html"
    queryset = Contact.objects.all()
    form_class = ContactModelForm
    success_url = reverse_lazy("cashflow:contactlist")


class ContactImportView(LoginRequiredMixin, TemplateView):
    """
    **ContactImportView(LoginRequiredMixin, TemplateView)**

    View to import Bankifi/Cashflow contacts from Xero.
    """ 
    template_name = "cashflow/contact/contact_import.html"

    def get_context_data(self, **kwargs):
        context = super(ContactImportView, self).get_context_data(**kwargs)
        
        if ON_HEROKU:
            # We can now create a Xero object that allows access to the API
            xero = get_xero(self.request)
            context['add_count'] = add_contacts(xero)
        
        return context


# === Methods ===

def add_contact(contact):
    """
    **add_contact(contact)**

    Add an imported contact from Xero

    **Parameters:**

    ***contact***: Xero contact to add to Bankifi.

    **Returns:**

    1 if contact was added or 0 if contact was not added.
    """ 
    count = 0
    bf_contact = Contact.objects.filter(contact_id=contact.get('ContactID', '')).first()
    if bf_contact is None:               
        bf_contact = Contact(name=contact.get('Name', ''), first_name=contact.get('FirstName', ''), 
            last_name=contact.get('LastName', ''), contact_id=contact.get('ContactID', ''))
        if bf_contact:
            bf_contact.save()
            count = 1

    return count


def add_contacts(xero):
    """
    **add_contacts(xero)**

    Add a list of imported contacts from Xero

    **Parameters:**

    ***xero***: Xero connection object.

    **Returns:**

    Number of contacts added to Bankifi
    """ 
    # Get a list of contacts to import from Xero
    contacts = xero.contacts.filter(ContactStatus='ACTIVE')
    count = 0
    
    for contact in contacts:
        # Import the contact into Bankifi
        count += add_contact(contact) 

    return count

