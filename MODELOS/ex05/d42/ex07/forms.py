from django import forms
from .models import Movies

class updateForm(forms.Form):
    movie = forms.ModelChoiceField(queryset=Movies.objects.all(),
    label="select a Movie")
    opening_crawl = forms.CharField(widget=forms.Textarea, label="New opening crawl")