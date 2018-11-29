from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.urls import reverse
from .functions import *


@login_required
def transaction_details(request, ide):
    tr = get_object_or_404(Transaction, pk=ide)
    type_, entity = related_entity(tr)
    if type_ == "event":
        base_template = "base_template_agenda.html"
    elif type_ == "group" :
        base_template = "base_template_groups.html"
    else:
        base_template = "base_template_friends.html"
    context = {
        'transaction' : tr,
        'type' : type_,
        'entity' : entity,
        'beneficiaries' : tr.beneficiaries.all(),
        'base_template' : base_template,
    }
    return render(request, 'transaction_details.html', context)
