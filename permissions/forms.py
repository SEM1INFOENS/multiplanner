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
        queryset=None,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', True)
        self.base_fields.get('members_field').required = required
        if 'label' in kwargs:
            label = kwargs.pop('label')
            self.base_fields.get('members_field').label = label
        if 'initial' in kwargs:
            initial_param = kwargs.pop('initial')
        else:
            initial_param = None
        queryset = kwargs.pop('queryset', User.objects.all())
        super().__init__(*args, **kwargs)
        self.fields['members_field'].queryset = queryset
        if self.instance.pk:
            self.initial['members_field'] = self.instance.all().values_list('pk', flat=True)
        else:
            if initial_param:
                self.initial['members_field'] = initial_param #[u.pk for u in initial]
            self.instance = PermGroup.create_new(commit=False)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        if instance.pk:
            instance.clear()
            instance.add(*self.cleaned_data['members_field'])
        return instance
