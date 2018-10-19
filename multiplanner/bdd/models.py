from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class User(models.Model):
    name = models.CharField(label='Gamertag', max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Gamertag', 'class': 'form-input'}))
    password = models.CharField(widget=forms.PasswordInput)
    email  = models.EmailField(max_length=200)

def validate_amount(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )
def to_choices(l):
    out = []
    for s in l:
        assert isinstance(s, str)
        out.append((a,a))
    return out

class Transaction(models.Models):
    motive = models.CharField(max_length=1000)
    expeditor = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiaries = 
    amount = models.FloatField(validators=[validate_amount])
    dependency_possibilities = ['group', 'event']
    dependency = models.CharField(choices = to_choices(dependency_possibilities))
- id_dependancy: id of the meeting in question if dependancy=1, id of the group if dependancy=2


Event

id
Date
Place
Creator
Administrators
Attendees
Invited


Friendships

id
User1
User2


Meeting:

id
The way constraints are implemented is still to be discussed.



Group

id
nom
id of the people


Creator
Administrators


Shared account:

id
members
