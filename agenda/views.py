from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.urls import reverse
from .forms import *
from django.utils import timezone
import datetime
from django.forms.formsets import formset_factory
from django.utils import timezone
from .models import *
from accounting import resolution

def date_format_ics(date, time):
    '''Converts date to date in ICS format'''
    def add_zeros(s, year=False):
        '''Adds the right number of zeros before the string s so that len(s) = 2 (4 if it is a year)'''
        if year:
            return (4 -len(s))*'0' + s

        return (2-len(s))*'0' + s

    if time == None:
        time = datetime.time.min

    s1 = str(date.year)
    s2 = str(date.month)
    s3 = str(date.day)
    s4 = str(time.hour)
    s5 = str(time.minute)
    s6 = str(time.second)
    return add_zeros(s1) + add_zeros(s2) + add_zeros(s3) + "T" + add_zeros(s4) + add_zeros(s5) + add_zeros(s6) + "Z"


@login_required
def create_event(request):
    context = {'new' : True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST, creator_user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            event = form.save()
            success = messages.success(request, 'Event successfully created')
            #warn = messages.warning(request, 'Event created')
            #error = messages.error(request, 'Event created')
            #info = messages.info(request, 'Event created')
            #debug = messages.debug(request, 'Event created')
            #all_m = [success, warn, info, error]

            #url_e = reverse('event', event.id)
            # redirect to a new URL:
            return redirect('event', ide=event.id)
            #return HttpResponseRedirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm(creator_user=request.user)

    context.update({'form': form})
    return render(request, 'edit_event.html', context)

@login_required
def edit_event(request, ide):
    context = {'new' : False}
    event = get_object_or_404(Event, pk=ide)
    user = request.user
    if user in event.administrators.all() : #user can only edit events of which he is admin
        if request.method == "POST":
            form = EventForm(request.POST, creator_user=event.creator, instance=event)
            if form.is_valid():
                event = form.save(commit=False)
                event.save() 

                success = messages.success(request, 'Event successfully modified')                
                return redirect('event', ide=event.id)
        else:
            form = EventForm(creator_user=event.creator, instance=event)
        context.update({'form': form, 'ide':event.id})
        return render(request, 'edit_event.html', context)
    else:
        raise PermissionDenied
    

@login_required
def agenda(request):
    user = request.user
    context = {
        'events_admin': Event.objects.filter(administrators=user),
        'events_invited': Event.objects.invited(user),
        'events_attendees': Event.objects.attending(user),
        'events_past': Event.objects.past(user),
    }
    return render(request, 'agenda.html', context)


#we should check if the user is allowed to see the event
@login_required
def event(request, ide):
    event = get_object_or_404(Event, pk=ide)
    group = event.attendees
    user = request.user

   

    if request.method == 'POST':
        form = TransactionForm(request.POST, current_group=group)
        
        if form.is_valid():
            transaction = form.save()
            success = messages.success(request, 'Transaction successfully created')
            return redirect('event', ide=event.id)
    else:
        form = TransactionForm(current_group=group)

    invited = event.invited.all()
    attendees = event.attendees.members.all()
    invited_attendees = [(u, (u in attendees)) for u in invited] 
    admin_l = event.administrators.all()
    last_transactions = event.attendees.transactions.all().order_by('-date')
    try :
        sitting_arrangement = event.sitting#.table__set.all()
    except Sitting.DoesNotExist:
        sitting_arrangement = None


    balance = resolution.balance_in_floats(group)
    balance1 = [b for b in balance]
    res = resolution.resolution_tuple(group,balance1)
    
    list_context =[]
    members = [m for m in group.members.all()]
    for i in range(len(balance)):
        list_context.append((members[i],balance[i]))



    context = {
        'event': event,
        'invited' : invited_attendees,
        'admin' : admin_l,
        'is_admin' : (request.user in admin_l),
        'can_accept_invite' : event.can_accept_invite(user),
        'can_cancel_acceptance' : event.can_cancel_acceptance(user),
        'last_transactions' : last_transactions,
        'form' : form,
        'sitting_arrangement' : sitting_arrangement,
        'list_context' : list_context,
        'resolution' : res ,
    }
    if event.is_over():
        messages.warning(request, 'This event is over')
    elif event.has_begun():
        messages.warning(request, 'This event has already begun')
    return render(request, 'event.html', context)

@login_required
def generate_calendar(request):
    # a = User.objects.create_user(username='bulbizarre3')
    # b = User.objects.create_user(username='salazemece3')
    # c = User.objects.create_user(username='carapueze3')

    # g = Group()
    # g.save()
    # g.members.add(*[a,b,c])

    # e1 = Event(
    #     name='myawesomeevent',
    #     date=timezone.now(),
    #     time=timezone.now(),
    #     place="ici",
    #     creator=a,
    #     attendees=g,
    #     )
    # e1.save()
    # e1.invited.add(*[a,b,c])
    # e1.administrators.add(a)

    # e2 = Event(
    #     name='myawesomeevent-thereturn',
    #     date=timezone.now(),
    #     time=timezone.now(),
    #     place="bloublou",
    #     creator=a,
    #     attendees=g,
    #     )
    # e2.save()
    # e2.invited.add(*[a,b,c])
    # e2.administrators.add(a)

    # e3 = Event(
    #     name='myawesomeevent-thereturnagain',
    #     date=timezone.now(),
    #     time=timezone.now(),
    #     place="là",
    #     creator=a,
    #     attendees=g,
    #     )
    # e3.save()
    # e3.invited.add(*[a,b,c])
    # e3.administrators.add(a)

    # user = a

    user = request.user
    list_event = Event.objects.filter(attendees__members=user)

    for event in list_event:
        event.date_start_ics = date_format_ics(event.date, event.time)
        event.date_end_ics = date_format_ics(event.date_end, event.time_end)

    response = HttpResponse(content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
    t = loader.get_template('calendar.ics')
    context = {
       'list_event': list_event,
    }
    response.write(t.render(context))
    return response


@login_required
def invitation_answer(request):
    assert request.method == 'POST'
    redirect_url = request.POST.get('redirect_url')
    user = request.user
    event = Event.objects.get(pk=request.POST.get('event'))
    if "accept_invite" in request.POST:
        event.accept_invite(user)
    if "cancel_acceptance" in request.POST:
        event.cancel_acceptance(user)

    return redirect(redirect_url)


@login_required
def new_sitting(request):
    assert request.method == 'POST'
    redirect_url = request.POST.get('redirect_url')
    event = Event.objects.get(pk=request.POST.get('event'))
    tables_str = request.POST.get('tables')
    tables = [int(s) for s in tables_str.split(',')]
    Sitting.set_new(event, tables)
    return redirect(redirect_url)
