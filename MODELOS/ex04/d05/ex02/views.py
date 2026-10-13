from django.shortcuts import render
from django.conf import settings
from .forms import TextInputForm
import datetime
import os
# Create your views here.

def ex02_view(request):
    form = TextInputForm()
    history = []
    if os.path.exists(settings.LOG_FILE_PATH):
        with open(settings.LOG_FILE_PATH, "r", encoding="utf-8") as file:
            history = file.readlines()

    if request.method == "POST":
        form = TextInputForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"{timestamp} - {text}\n"

            with open(settings.LOG_FILE_PATH, "a", encoding="utf-8") as file:
                file.write(entry)
            history.append(entry)
    
    return render(request, "ex02/index.html", {"form": form, "history": history})