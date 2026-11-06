from django.shortcuts import render, redirect
from django.conf import settings 
from django.contrib import auth 
from random import choice
from .models import Tips
from . import forms 

# Create your views here.
def main(request):
    tmptips = forms.TipForm()

    response = render(request, 'ex/index.html', {'tips': tmptips})
    if not request.COOKIES.get('username'):
        randouser = choice(settings.LIST_OF_USER)
        request.COOKIES['username'] = randouser
        response = render(request, 'ex/index.html', {'tips': tmptips })
        response.set_cookie('username', randouser, max_age=5)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('up') or request.POST.get('down'):
                db_tip = Tips.objects.get(pk=request.POST.get('up') or request.POST.get('down'))
                if request.POST.get('up'):
                    db_tip.upvote(request.user)
                else:
                    db_tip.downvote(request.user)
            if request.POST.get('delete'):
                if request.user.has_perm('ex.delete_tips') or Tips.objects.get(pk=request.POST.get('delete').author == request.user):
                    Tips(pk=request.POST.get('delete')).delete()
            tips = forms.TipForm(request.POST)
            if tips.is_valid():
                db_tip = Tips.objects.create(
                    content=tips.cleaned_data['content'],
                    author=request.user,
                ) 
                db_tip.save()
        tips_content = Tips.objects.all()
        return render(request, 'ex/index.html', {'tips': tmptips, 'tips_content': tips_content})
    return response

def register(request):
    regist = forms.Register()

    if request.method == 'POST':
        regist = forms.Register(request.POST)
        if regist.is_valid():
            user = auth.get_user_model().objects.create_user(
                username=regist.cleaned_data['username'],
                password=regist.cleaned_data['password'],
            )
            if not user:
                return render(request, 'ex/register.html', {'regist': regist})
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/register.html', {'regist': regist})

def login(request):
    log = forms.Login()
    if request.method == "POST":
        log = forms.Login(request.POST)
        if log.is_valid():
            user = auth.authenticate(
                username=log.cleaned_data['username'],
                password=log.cleaned_data['password'],
            )
            auth.login(request, user)
            return redirect('/')
    return render(request, 'ex/login.html', {'login': log})

def logout(request):
    auth.logout(request) 
    return redirect('/')