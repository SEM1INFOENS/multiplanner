from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            form.save()
            # redirect to a new URL:
            return redirect('/agenda/')
            #return HttpResponseRedirect('/user/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EventForm(creator_user=request.user)

    return render(request, 'new_event.html', {'form': form})


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

