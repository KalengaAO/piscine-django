from django.shortcuts import render, redirect
from django.conf import settings 
from random import choice 
from django.contrib import auth 
from django.contrib.auth.decorators import login_required
from . import forms 
from .models import Tip
from django.views.decorators.csrf import csrf_exempt 
# Create your views here.

def main(request):
    form = forms.TipForm()
    
    if not request.COOKIES.get('username'):
        request.COOKIES['username'] = choice(settings.LIST_OF_USER)
        randomuser = choice(settings.LIST_OF_USER)
        response = render(request, 'ex/main.html', {'form': form})
        response.set_cookie('username', randomuser, max_age=42)
        return response

    if request.user.is_authenticated:
        if request.method == 'POST':
            tip = forms.TipForm(request.POST)
            if tip.is_valid():
                tipcontent = Tip(
                                content=tip.cleaned_data.get('content'),
                                author=request.user)
                tipcontent.save()
    tips = Tip.objects.all()
    return render(request, 'ex/main.html', {'form': form, 'tip': tips})

@csrf_exempt
def login(request):
    login = forms.Login()
   
    if request.method == 'POST':
        login = forms.Login(request.POST)
        if login.is_valid():
            user = auth.authenticate(
                username=login.cleaned_data['username'],
                password=login.cleaned_data['password'],
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/login.html', {'forms': login})


def register(request):
    regist = forms.Register()
    user = {}
    if request.method == 'POST':
        regist = forms.Register(request.POST)
        if regist.is_valid():
            user = auth.get_user_model().objects.create_user(
                username=regist.cleaned_data['username'],
                password=regist.cleaned_data['password'],
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/register.html', {'forms': regist})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')