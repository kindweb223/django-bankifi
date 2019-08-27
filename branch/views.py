import requests
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.generic import (
    DetailView, 
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView,
    )

@login_required
def branch(request): 
    template = "branch/branches.html"
    postcode = request.GET.get("postcode", None)

    if postcode is not None:
        return render(request, template, {'branches': get_branches(postcode.strip())})
    else:
        return render(request, template, {})

def get_branches(code):
    url = "https://api.hsbc.com/x-open-banking/v1.0/branches/postcode/{0}".format(code)

    branches = {}
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        decoded_data = r.content.decode('utf-8')
        branches = json.loads(decoded_data) 
        for branch in branches:
            branch['mapaddress'] = get_address(branch)
            branch['Monday'] = get_times(branch, "Monday")
            branch['Tuesday'] = get_times(branch, "Tuesday")
            branch['Wednesday'] = get_times(branch, "Wednesday")
            branch['Thursday'] = get_times(branch, "Thursday")
            branch['Friday'] = get_times(branch, "Friday")
            branch['Saturday'] = get_times(branch, "Saturday")
            branch['Sunday'] = get_times(branch, "Sunnday")
            branch['ATM'] = branch.get('ServicesFacilities').get('AtmAtBranch')

    return branches


def get_times(branch, day):
    open_key = "{0}OpeningTime".format(day)
    close_key = "{0}ClosingTime".format(day)
    available = branch.get('Availability')
    if available.get(open_key) is not None and available.get(open_key) != '':
        return "{0} - {1}".format(available.get(open_key)[:-3], available.get(close_key)[:-3])
    else:
        return "Closed"


def get_address(branch): 
    return "UK, {0}, {1}".format(branch.get('Location').get('TownName'), branch.get('Location').get('StreetName')) 
    
