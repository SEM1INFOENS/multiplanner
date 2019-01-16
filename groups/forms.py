from django import forms
from django.forms import ModelForm, Form, modelform_factory
from django.db.models import Q

from .models import *
import accounting.models


class GroupForm(ModelForm):

    class Meta :
        model = Group
        fields = ['name', 'public','currency']

    def __init__(self, *args, **kwargs):
        self._user =  kwargs.pop('creator_user')
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

    def save(self, commit=True):
        inst = super(GroupForm, self).save(commit=False)
        if commit:
            inst.save()
        return inst


class GroupInviteForm(Form):

    users = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        self._group = kwargs.pop('current_group')
        super().__init__(*args, **kwargs)

        # filter the QuerySet such that
        # we can not invite members or users already invited :
        gp_mem = self._group.members.all().values_list('pk', flat=True)
        gp_inv = GroupInvite.users_invited(self._group)
        qs = User.objects.exclude(pk__in=gp_mem).exclude(pk__in=gp_inv)
        self.fields['users'].queryset = qs

    def save(self):
        for u in self.cleaned_data['users']:
            GroupInvite.create_new(self._group, u)
