from django import forms
from django.forms import ModelForm, Form, modelform_factory
from django.contrib.admin import widgets
#from treasuremap.forms import LatLongField
#from treasuremap import widgets as tmw
from .models import *

# Form : to create a form
# ModelForm : to automaticaly create a form from a model
# modelform_factory : same as ModelForm but shorter

class EventForm(ModelForm):

    #place = LatLongField()
    # I was not able to make it work...
    # https://github.com/silentsokolov/django-treasuremap
    
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'place', 'administrators', 'invited']
        widgets = {
            'description' : forms.Textarea,
            'time' : forms.TimeInput(format='%H:%M'),
            'date' : forms.SelectDateWidget(), #bof
            #'time' : widgets.AdminTimeWidget(),
            #'date' :  widgets.AdminDateWidget(), #top!
            # https://gilang.chandrasa.com/blog/using-django-admin-datepicker-in-custom-form/
        }
        field_classes = {}
        labels = {}
        help_texts = {}
        error_messages = {}

    def __init__(self, *args, **kwargs):
        self._user =  kwargs.pop('creator_user')
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(EventForm, self).save(commit=False)
        inst.creator = self._user  # we set 'Event.creator' to the currently logged in user
        if commit:
            inst.save()
            self.save_m2m()
        return inst
