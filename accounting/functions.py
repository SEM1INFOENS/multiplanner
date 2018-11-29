from .models import Transaction
from groups.models import Group
from agenda.models import Event

def related_entity(transaction):
    try:
        group = Group.objects.get(transactions=transaction)
        try:
            event = group.event
            return ('event', event)
        except Event.DoesNotExist:
            return ('group', group)
    except Group.DoesNotExist:
        return ('', None)
