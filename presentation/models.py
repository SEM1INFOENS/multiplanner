'''Models for the presentation app'''

from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import CurrencyField
from djmoney.settings import CURRENCY_CHOICES, DEFAULT_CURRENCY

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_currency = CurrencyField(default=DEFAULT_CURRENCY, choices=CURRENCY_CHOICES)

    notif_invited_to_event = models.BooleanField(default=True)
    notif_requested_by_one_user = models.BooleanField(default=True)
    notif_upcoming_event = models.BooleanField(default=True)
    notif_edited_event = models.BooleanField(default=True)
    
    @classmethod
    def get_or_create(cls, user, *args, **kwargs):
        try:
            profile = cls.objects.get(user=user)
            return profile
        except cls.DoesNotExist:
            return cls(user=user, *args, **kwargs)
