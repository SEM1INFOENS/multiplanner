from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.urls import reverse
from .forms import *
from accounting.forms import TransactionForm
import datetime
from django.forms.formsets import formset_factory
from django.utils import timezone
from .models import *
from accounting import resolution

from guardian.decorators import permission_required_or_403
from permissions.utils import get_default_permission_name
from permissions.forms import PermGroupForm
from .functions import date_format_ics

from notify.signals import notify

@login_required
def create_event(request):
    context = {'new' : True}
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST, creator_user=request.user, new=True)
        admins_form = PermGroupForm(request.POST)
        invited_form = PermGroupForm(request.POST)
        # check whether it's valid:
        if form.is_valid() and admins_form.is_valid() and invited_form.is_valid():
            # process the data in form.cleaned_data as required
            form.instance.admins = admins_form.save()
            form.instance.invited = invited_form.save()
            event = form.save()

            success = messages.success(request, 'Event successfully created')
            #warn = messages.warning(request, 'Event created')
            #error = messages.error(request, 'Event created')
            #info = messages.info(request, 'Event created')
            #debug = messages.debug(request, 'Event created')
            #all_m = [success, warn, info, error]
            for u in event.invited.iterator():
                notify.send(request.user, recipient = u, actor=request.user, verb = 'has invited you to an event.', nf_type = 'invited_to_event')
            #url_e = reverse('event', event.id)
            # redirect to a new URL:
            return redirect('event', ide=event.id)
            #return HttpResponseRedirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm(creator_user=request.user, new=True)
        admins_form = PermGroupForm(label='admins', initial=[request.user])
        invited_form = PermGroupForm(label='invited')

    context.update({'form': form, 'admins_form': admins_form, 'invited_form': invited_form})
    return render(request, 'edit_event.html', context)


change_perm = get_default_permission_name(Event, 'change')
@login_required
@permission_required_or_403(change_perm, (Event, 'pk', 'ide'), accept_global_perms=True)
def edit_event(request, ide):
    context = {'new' : False}
    event = get_object_or_404(Event, pk=ide)
    user = request.user
    if request.method == "POST":
        form = EventForm(request.POST, creator_user=event.creator, new=False, instance=event)
        admins_form = PermGroupForm(request.POST, instance=event.admins, prefix='admins')
        invited_form = PermGroupForm(request.POST, instance=event.invited)
        if form.is_valid() and admins_form.is_valid() and invited_form.is_valid():
            admins_form.save()
            invited_form.save()
            event = form.save(commit=False)
            event.save()
            
            group = event.attendees
            # If the number of members changes then update balances in event
            balances = Balance.objects.balancesOfGroup(group)     
            u = []
            for b in balances:
                if b.user not in group.members.all():
                    b.delete()
                else:
                    u.append(b.user)
            for m in group.members.all():
                if m not in u:
                    b = Balance(user=m,group = group,amount = Money(0,group.currency))
                    b.save()

            success = messages.success(request, 'Event successfully modified')
            return redirect('event', ide=event.id)
    else:
        form = EventForm(creator_user=event.creator, new=False, instance=event)
        admins_form = PermGroupForm(label='admins', instance=event.admins, prefix='admins')
        invited_form = PermGroupForm(label='invited', instance=event.invited)
    context.update({'form': form, 'ide':event.id,
    'admins_form': admins_form, 'invited_form': invited_form})
    return render(request, 'edit_event.html', context)


@login_required
def agenda(request):
    user = request.user
    context = {
        #'events_admin': Event.objects.filter(admins__members=user),
        #'events_invited': Event.objects.invited(user),
        #'events_attendees': Event.objects.attending(user),
        #'events_past': Event.objects.past(user),
        'username' : user.username,
        'events' : Event.objects.json_list(user),
    }
    return render(request, 'agenda.html', context)


view_perm = get_default_permission_name(Event, 'view')
@login_required
@permission_required_or_403(view_perm, (Event, 'pk', 'ide'), accept_global_perms=True)
def event(request, ide):
    event = get_object_or_404(Event, pk=ide)
    group = event.attendees
    user = request.user

    if request.method == 'POST':
        form = TransactionForm(request.POST, current_group=group, between_members=False)

        if form.is_valid():
            transaction = form.save()
            success = messages.success(request, 'Transaction successfully created')
            return redirect('event', ide=event.id)
    else:
        form = TransactionForm(current_group=group, between_members=True)

    invited = event.invited.all()
    attendees = event.attendees.members.all()
    invited_attendees = [(u, (u in attendees)) for u in invited]
    admin_l = event.admins.all()
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
    perm_name = get_default_permission_name(Event,'change')
    can_edit = request.user.has_perm(perm_name) or request.user.has_perm(perm_name, event)

    context = {
        'event': event,
        'invited' : invited_attendees,
        'admin' : admin_l,
        'can_edit' : can_edit,
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

#@login_required
def generate_calendar(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        list_event = Event.objects.attending_all(user)

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
    if "decline_invite" in request.POST:
        event.decline_invite(user)
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
