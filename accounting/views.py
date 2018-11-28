from django.shortcuts import render

# Create your views here.
def showGroups (request):
	return render(request, 'index.html')
