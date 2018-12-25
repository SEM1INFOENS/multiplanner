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
