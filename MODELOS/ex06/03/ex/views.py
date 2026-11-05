from django.shortcuts import render, redirect
from random import choice
from django.conf import settings 
from . import forms 
from .models import Tip
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def main(request):
    tmptips = forms.TipForm()

    if not request.COOKIES.get('username'):
        raandomuser = choice(settings.LIST_USER)
        request.COOKIES['username'] = raandomuser
        response = render(request, 'ex/main.html', {'tips': tmptips})
        response.set_cookie('username', raandomuser, max_age=42)
        return response

    if request.user.is_authenticated:
        try:
            if request.method == 'POST':
                if request.POST.get('up') or request.POST.get('down'):
                    tip = Tip.objects.get(pk=request.POST.get('up') or request.POST.get('down'))
                    if request.POST.get('up'):
                        tip.upvote(request.user)
                    else:
                        tip.downvote(request.user)
                if request.POST.get('delete'):
                    Tip.objects.get(pk=request.POST.get('delete')).delete()
                tips = forms.TipForm(request.POST)
                if tips.is_valid():
                    db_Tips = Tip(content=tips.cleaned_data.get('content'),
                    author=request.user,
                    )
                    db_Tips.save()
            tips_content = Tip.objects.all()
            return render(request, 'ex/main.html', {'tips': tmptips, 'tips_content': tips_content})
        except Tip.DoesNotExist:
            pass 
    return render(request, 'ex/main.html', {'tips': tmptips})

def register(request):
    regist = forms.Register()

    if request.method == 'POST':
        regist = forms.Register(request.POST)
        if regist.is_valid():
            user = auth.get_user_model().objects.create_user(
                username=regist.cleaned_data.get('username'),
                password=regist.cleaned_data.get('password'),
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/register.html', {'register': regist})

def login(request):
    log = forms.Login()

    if request.method == 'POST':
        log = forms.Login(request.POST)
        if log.is_valid():
            user = auth.authenticate(
                username=log.cleaned_data.get('username'),
                password=log.cleaned_data.get('password'),
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/login.html', {'login': log})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


