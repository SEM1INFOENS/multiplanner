from django.shortcuts import render

from django.contrib.auth.models import User

from accounting.models import Transaction

def index(request):
    context = {'users': User.objects.all()}
    return render(request, 'users/index.html', context)

def page(request, username):
    context = {'transactions': Transaction.objects.filter(payer=User.objects.get(username=username)),
               'username': username}
    return render(request, 'users/page.html', context)
