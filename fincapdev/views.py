from django.shortcuts import render, redirect

########## PAGES ##########

def landing(request):
    return render(request, 'landing.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def network_view(request):
	return render(request, 'network_view.html')

########## FUNCTIONS ##########