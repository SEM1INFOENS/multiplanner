from django import forms
from django.forms import ModelForm
from .models import *



class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = [] #'motive', 'date', 'payer', 'amount', 'beneficiaries']
        widgets = {
            'motive' : forms.Textarea,
            'date' : forms.SelectDateWidget(),
            'amoint' : forms.NumberInput
        }

    def __init__(self, *args, **kwargs):
        self._group = kwargs.pop('current_group')
        between_members = kwargs.pop('between_members')
        super(TransactionForm, self).__init__(*args, **kwargs)

        # if between_members:
        #     self.fields['payer'].queryset = self._group.members
        #     self.fields['beneficiaries'].queryset = self._group.members

    def save(self, commit=True):
        inst = super(TransactionForm, self).save()
        self._group.transactions.add(inst)
        self._group.save()

        return inst
