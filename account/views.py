from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clear_data = form.cleaned_data
            user = authenticate(request, 
                                username = clear_data['username'], 
                                password = clear_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfuly')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', { 'login_form': form })

@login_required
def home(request):
    return render(request, 'account/index.html', {'section': 'dashboard'})