from django.forms import ModelForm
from .models import UserProfile


class UserSettingsForm(ModelForm):
    '''form to edit the UserProfile instances '''

    class Meta:
        model = UserProfile
        fields = ['default_currency', 'notif_invited_to_event', 'notif_requested_by_one_user', 'notif_upcoming_event', 'notif_edited_event']
