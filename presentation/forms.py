from django.forms import ModelForm
from .models import UserProfile


class UserSettingsForm(ModelForm):
    '''form to edit the UserProfile instances '''

    class Meta:
        model = UserProfile
        fields = ['default_currency']
