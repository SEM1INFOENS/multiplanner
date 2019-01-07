''' Test set for the agenda app '''

from django.test import TestCase
from django.utils import timezone
from agenda.models import *
from groups.models import *
from accounting.models import *
import datetime
from .sit import *


class AgendaTestCase(TestCase):
    print("\n\n - running tests for the agenda app:\n")

    users_list = []
    event_list=[]

    def setUp(self):
        #two ways to create users (one doesn't need .save() ):
        a = User.objects.create_user(username='alice')
        b = User.objects.create_user(username='bob')
        c = User(username='carllotta')
        d = User(username = 'david')
        e = User(username='emily')
        f = User(username='fred')
        e.save()
        f.save()
        c.save()
        d.save()
        self.users_list = [a,b,c,d,e,f,]

        g1 = Group.create_for_event()
        g1.members.add(*[a,b,c,d,])

        g2 = Group.create_for_event()
        g2.members.add(*[a,b,c,d,e,f,])

        m1 = SecretMark.create_new(a, b, -10)
        m1.save()

        m2 = SecretMark.create_new(b,c,-10)
        m2.save()

        m3 = SecretMark.create_new(e, c, 10)
        m3.save()

        e1 = Event.create_new(
            date=timezone.now(),
            time=timezone.now(),
            date_end=timezone.now()+datetime.timedelta(days=1),
            time_end=timezone.now()+datetime.timedelta(hours=1),
            #place="ici",
            creator=a,
            attendees=g1,
        )
        e1.invited.add(*[a,b,c,d])
        e1.admins.add(a)

        e2 = Event.create_new(
            date=timezone.now(),
            time=timezone.now(),
            date_end=timezone.now() + datetime.timedelta(days=1),
            time_end=timezone.now() + datetime.timedelta(hours=1),
            # place="ici",
            creator=a,
            attendees=g2,
        )
        e2.save()
        e2.invited.add(*[a, b, c, d,e ,f ,])
        e2.admins.add(a)

        self.event_list=[e1,e2]

    def test_event(self):
        for e in Event.objects.all():
            print(e.__repr__())
            assert (e in self.event_list)

    def test_sitting(self):
        tables = [2,2]
        #Case with 4 people
        assignements = sitting(self.event_list[0],tables)
        assi = lambda i : assignements[self.event_list[0].attendees.members.all()[i]]

        assert(assi(0) == assi(2))
        assert(assi(1) != assi(0))
        assert(assi(1) == assi(3))

        #Case with 6 people

        tables = [3,3]

        assignements = sitting(self.event_list[1],tables)
        assi = lambda i : assignements[self.event_list[1].attendees.members.all()[i]]

        assert(assi(0) == assi(2))
        assert(assi(2) ==  assi(4))
        assert(assi(1) != assi(0))
        assert(assi(1) == assi(3))
        assert(assi(3) == assi(5))



class EventPermissionsTestCase(TestCase):

    def setUp(self):
        aa = User.objects.create_user('app_admin')
        a = User.objects.create_user('admin')
        m = User.objects.create_user('member')
        u = User.objects.create_user('user')

        # The users should have been added to the folowing groups
        # by the signup view
        from permissions.group import admins, users
        admins.user_set.add(aa)
        users.user_set.add(a, m, u)

        from django.utils import timezone
        t = timezone.now()
        Event.create_new(t, t, t, t, a, invited=[a,m], admins=[a], public=False)

    def test(self):
        from permissions.utils import get_default_permission_name
        has_perm = lambda u, p, i : (u.has_perm(p,i) or u.has_perm(p))
        gp = Event.objects.get(pk=1)
        view_perm = get_default_permission_name(Event, 'view')
        change_perm = get_default_permission_name(Event, 'change')

        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert not has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)

        gp.public = True
        gp.save()
        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)

        gp.public = False
        gp.save()
        aa = User.objects.get(username='app_admin')
        a = User.objects.get(username='admin')
        m = User.objects.get(username='member')
        u = User.objects.get(username='user')
        assert has_perm(aa, view_perm, gp)
        assert has_perm(a, view_perm, gp)
        assert has_perm(m, view_perm, gp)
        assert not has_perm(u, view_perm, gp)
        assert has_perm(aa, change_perm, gp)
        assert has_perm(a, change_perm, gp)
        assert not has_perm(m, change_perm, gp)
        assert not has_perm(u, change_perm, gp)
