from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.urls import reverse
from .functions import *
from .forms import *

from django.forms import modelformset_factory

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

    TransactionFormSet = modelformset_factory(TransactionPart, fields=['amount'], extra=0, formset=EditTransactionFormSet)
    
    if request.method == 'POST':
        formset = TransactionFormSet(request.POST, queryset=tr.transactionpart_set.all(), amount=tr.amount)
        
        if formset.is_valid():
            formset.save()
    else:
        formset = TransactionFormSet(queryset=tr.transactionpart_set.all(), amount=tr.amount)
        

    context = {
        'transaction' : tr,
        'id' : ide,
        'transactions': tr.transactionpart_set.all(),
        'form' : formset,
        'transactions_forms' : zip(tr.get_beneficiaries(), formset),
        'type' : type_,
        'entity' : entity,
        'beneficiaries' : tr.get_beneficiaries(),
        'base_template' : base_template,
    }
    return render(request, 'transaction_details.html', context)
