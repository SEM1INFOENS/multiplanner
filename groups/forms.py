from django import forms
from django.forms import ModelForm, Form, modelform_factory

from .models import *
import accounting.models


class GroupForm (ModelForm):

    class Meta :
        model = Group
        fields = ['name','members']

    def __init__(self, *args, **kwargs):
        self._user =  kwargs.pop('creator_user')
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['members'].required = True

    def save(self, commit=True):
        inst = super(GroupForm, self).save()
        inst.save()
        return inst




class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['motive', 'date', 'payer', 'amount', 'beneficiaries']
        widgets = {
	    'motive' : forms.Textarea,
	    'date' : forms.SelectDateWidget(),
	    'amount' : forms.NumberInput
	}

    def __init__(self, *args, **kwargs):
        self._group = kwargs.pop('current_group')
        super(TransactionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(TransactionForm, self).save()
        self._group.transactions.add(inst)
        self._group.save()
        return inst
