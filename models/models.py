from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class User(models.Model):
    name = models.CharField(label='Gamertag', max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Gamertag', 'class': 'form-input'}))
    password = models.CharField(widget=forms.PasswordInput)
    email  = models.EmailField(max_length=200)

class Group(models.Models):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    
def validate_amount(value):
    try:
        assert (value >= 0.0)
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not a positive integer or a float  number'),
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
    date = models.DateTimeField()
    expeditor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[validate_amount])

class Transaction_1to1(Transaction):
    beneficiaire = models.ForeignKey(User, on_delete=models.CASCADE)

class Transaction_1toGroup(Transaction):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    

class Event(models.Models):
    date = models.DateTimeField()
    place = models.CharField(max_length=500, blank=True)
    #place spécification could be better: GPS coordonates...?
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    administrators = models.ManyToManyField(User)
    attendees = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited = models.ManyToManyField(User)


class Friendships(models.Models):
    User =    models.ForeignKey(User, on_delete=models.CASCADE)
    Friend =  models.ForeignKey(User, on_delete=models.CASCADE)
    status_possibilities = ['friends', 'invited']
    status = models.CharField(choices=to_choices(status_possibilities))

class Meeting(models.Models):
minimum_delay
maximum_delay
duration
possible_time_ranges

The way constraints are implemented is still to be discussed.



Creator
Administrators


Shared account:

id
members
