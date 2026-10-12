from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, "ex01/index.html")

def django_page(request):
    return render(request, "ex01/django.html", {"title" : "Ex01: Django, Web Framework."})

def display_pag(request):
    return render(request, "ex01/display.html", {"title" : "Ex01: Display Process of a Static Page."})

def templates_pag(request):
    return render(request, "ex01/templates.html", {"title" : "Ex01: Template Engine."})