''' Test set for the agenda app '''

from django.test import TestCase
from django.utils import timezone
from agenda.models import *
from groups.models import *
import datetime
#from .sitting import sitting_arrang


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
            time=timezone.now(),
            date_end=timezone.now()+datetime.timedelta(days=1),
            time_end=timezone.now()+datetime.timedelta(hours=1),
            #place="ici",
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

    #def test_sitting(self):
    #    m1 = SecretMark.create_new(a, b, -10)
    #    m1.save()

    #    tables = [2,2]

    #    assi = sitting_arrang(e1,tables)

    #    assert(assi[0] == assi[2])
    #    assert(assi[1] == assi[0])