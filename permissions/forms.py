''' form about permissions '''
from django.contrib.auth.models import User
from django import forms
from .models import PermGroup



class PermGroupForm(forms.ModelForm):
    ''' A form to fill a PermGroup object '''
    class Meta:
        model = PermGroup
        fields = []

    members_field = forms.ModelMultipleChoiceField(
        User.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        self.base_fields.get('members_field').required = required
        if 'label' in kwargs:
            label = kwargs.pop('label')
            self.base_fields.get('members_field').label = label
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['members_field'] = self.instance.all().values_list('pk', flat=True)
        else:
            self.instance = PermGroup.create_new(commit=False)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.pk:
            instance.clear()
            instance.add(*self.cleaned_data['members_field'])
        return instance
