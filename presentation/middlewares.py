from django.utils import timezone

from datetime import timedelta

from agenda.models import Event
from presentation.models import UserProfile

from notify.models import Notification
from notify.signals import notify

import math

INITIAL_DELAY_SECONDS = 24*3600 #the first notification for an upcoming event is sent INITIAL_DELAY_SECONDS seconds before the beginning of
# the event

def notifications(user):
    profile = UserProfile.objects.get(user=user)
    if profile.notif_upcoming_event:
        for notif in Notification.objects.filter(recipient=user, read=True):
            event = notif.actor#the only 'read' notifications are upcoming_event ones, the others are immediately deleted
            event.notifications_sent = -1
            notif.delete()
            event.save()


        for e in Event.objects.attending(user):
            nb_days = (e.date_time() - timezone.now()).days
            nb_minutes = (e.date_time() - timezone.now()).seconds /60
            nb_hours = nb_minutes/60

            #print('delay', e.date_time() - timezone.now(), (e.date_time() - timezone.now()).total_seconds())
            seconds_before_event = (e.date_time() - timezone.now()).total_seconds()
            
            if (e.notifications_sent != -1) and not(e.has_begun()) and \
            (seconds_before_event < 1/(2**e.notifications_sent)*INITIAL_DELAY_SECONDS) and (seconds_before_event >= 5 * 60):
                e.notifications_sent = math.floor(math.log2(INITIAL_DELAY_SECONDS/seconds_before_event)) + 1
                e.save()
                notify.send(user, recipient = user, actor=e, \
                    verb = 'is in %d hours and %d minutes from now.' % (nb_hours,nb_minutes%60), nf_type = 'upcoming_event')

            
def middleware_notifications(get_response):

    def middleware(request):
        
        try:#avoids problems if no user is logged in
            notifications(request.user)
        except:
            pass

        response = get_response(request)


        return response

    return middleware