from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .forms import *

@login_required
def create_event(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EventForm(request.POST, creator_user=request.user)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            event = form.save()
            success = messages.success(request, 'Event successfully created')
            warn = messages.warning(request, 'Event created')
            error = messages.error(request, 'Event created')
            info = messages.info(request, 'Event created')
            debug = messages.debug(request, 'Event created')
            all_m = [success, warn, info, error]

            #url_e = reverse('event', event.id)
            # redirect to a new URL:
            return redirect('event', ide=event.id) #, {'messages': [success]})
            #return HttpResponseRedirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm(creator_user=request.user)

    return render(request, 'edit_event.html', {'form': form})

@login_required
def edit_event(request, ide):
    event = get_object_or_404(Event, pk=ide)
    user = request.user
    if user in Event.objects.get(pk=ide).administrators.all() : #user can only edit events of which he is admin
        if request.method == "POST":
            form = EventForm(request.POST, instance=event, creator_user=request.user)
            if form.is_valid():
                event = form.save(commit=False)
                #event.save() # here a new event is saved, but it is not what we want.. 

                success = messages.success(request, 'Event successfully modified')                
                return redirect('event', ide=event.id)
        else:
            form = EventForm(instance=event, creator_user=request.user)
        return render(request, 'edit_event.html', {'form': form})
    else:
        raise PermissionDenied
    

@login_required
def agenda(request):
    user = request.user
    att = Event.objects.filter(attendees__members=user)
    context = {
        'events_admin': Event.objects.filter(administrators=user),
        'events_invited': Event.objects.filter(invited=user),
        'events_attendees': att,
    }
    return render(request, 'agenda.html', context)


#we should check if the user is allowed to see the event
@login_required
def event(request, ide):
    event = get_object_or_404(Event, pk=ide)
    admin_l = event.administrators.all()
    context = {
        'event': event,
        'invited' : event.invited.all(),
        'admin' : admin_l,
        'is_admin' : (request.user in admin_l), 
    }
    return render(request, 'event.html', context)

