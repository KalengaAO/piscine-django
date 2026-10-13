from django import forms

class TextInputForm(forms.Form):
    text = forms.CharField(label="Imput Text", max_length=200)