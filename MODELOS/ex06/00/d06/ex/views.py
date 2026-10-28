from django.shortcuts import render
from django.conf import settings
from random import choice

# Create your views here.
def main(request):
    response = render(request, "ex/index.html")
    if not request.COOKIES.get('username'):
        random_user = choice(settings.USER_POOL)
        request.COOKIES['username'] =  random_user
        response = render(request, "ex/index.html")
        response.set_cookie('username', random_user, max_age=42)
    return response 