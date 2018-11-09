from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounting.models import Transaction

@login_required
def index(request):
    context = {'users': User.objects.all()}
    return render(request, 'users/index.html', context)

@login_required
def page(request, username):
    context = {'transactions': Transaction.objects.filter(payer=User.objects.get(username=username)),
               'username': username}
    return render(request, 'users/page.html', context)

def login(request):
    return render(request, 'users/login.html', {})
