from django import forms
from django.forms import ModelForm
from djmoney.utils import Money
from .models import *
from math import ceil



class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['motive', 'date', 'payer', 'amount'] #'motive', 'date', 'payer', 'amount', 'beneficiaries']
        widgets = {
            'date' : forms.SelectDateWidget(),
        }

    def __init__(self, *args, **kwargs):
        self._group = kwargs.pop('current_group')
        between_members = kwargs.pop('between_members')
        super(TransactionForm, self).__init__(*args, **kwargs)

        if between_members:
            self.fields['payer'].queryset = self._group.members
            #self.fields['beneficiaries'].queryset = self._group.members

    def save(self, commit=True):
        inst = super(TransactionForm, self).save()
        self._group.transactions.add(inst)
        self._group.save()
        
        base = Money(ceil(inst.amount/len(self._group.members.all())*100)/100, inst.amount.currency)

        parts = [base for _ in self._group.members.all()]

        if (sum(parts) != inst.amount):
            parts[-1]+= inst.amount - sum(parts)

        for (member, part) in zip(self._group.members.all(), parts):
            tr = TransactionPart()
            tr.transaction = inst
            tr.beneficiary = member
            tr.amount = part
            tr.save()

        return inst
