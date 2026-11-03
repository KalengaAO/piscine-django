from django.shortcuts import render, redirect
from django.conf import settings 
from random import choice 
from django.contrib import auth
from django.contrib.auth.decorators import login_required 
from . import forms
# Create your views here.

def main(request):
    if not request.COOKIES.get('username'):
        randomusername = choice(settings.USER_POOL)
        request.COOKIES['username'] = randomusername
        response = render(request, 'ex/index.html', {'home':'home', 'username': randomusername})
        response.set_cookie('username', randomusername, max_age=42)
        return response
    return render(request, 'ex/index.html', {'home': 'home'})

def login(request):

    login = forms.Login()
    if request.method == "POST":
        login = forms.Login(request.POST)

        if login.is_valid():
            user = auth.authenticate(
                username=login.cleaned_data['username'],
                password=login.cleaned_data['password']
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/login.html', {'forms': login})

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register = forms.Register()
    if request.method == 'POST':
        register = forms.Register(request.POST)
        if register.is_valid():
            user = auth.get_user_model().objects.create_user(
                username=register.cleaned_data['username'],
                password=register.cleaned_data['password']
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/register.html', {'forms': register })

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')