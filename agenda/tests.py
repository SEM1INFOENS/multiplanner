''' Test set for the agenda app '''

from django.test import TestCase
from django.utils import timezone
from agenda.models import *
from groups.models import *


class AgendaTestCase(TestCase):
    print("\n\n - running tests for the agenda app:\n")
    
    users_list = []
    event_list=[]
    
    def setUp(self):
        #two ways to create users (one doesn't need .save() ):
        a = User.objects.create_user(username='alice')
        b = User.objects.create_user(username='bob')
        c = User(username='carllotta')
        c.save()
        self.users_list = [a,b,c,]

        g = Group()
        g.save()
        g.members.add(*[a,b,c])

        e1 = Event(
            date=timezone.now(),
            place="ici",
            creator=a,
            attendees=g,
        )
        e1.save()
        e1.invited.add(*[a,b,c])
        e1.administrators.add(a)
        self.event_list=[e1]

    def test_event(self):
        for e in Event.objects.all():
            print(e.__repr__())
            assert (e in self.event_list)
                       

