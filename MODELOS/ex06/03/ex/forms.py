from django import forms 
from django.contrib.auth import get_user_model, authenticate
from . import models 

class Register(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())

    def clean(self):
        super(Register, self).clean()

        try:
            get_user_model().objects.get(username=self.cleaned_data.get('username'))
            self.add_error('username', 'This user name already exists!') 
        except get_user_model().DoesNotExist:
            pass

        if self.cleaned_data.get('password') != self.cleaned_data.get('confirm_password'):
            self.add_error('confirm_password', 'The password does not match!')

class Login(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())

    def clean(self):
        super(Login, self).clean()

        if not authenticate(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password'),
        ):
            self.add_error('password', 'wrong password')
            self.add_error('username', 'wrong username')

class TipForm(forms.ModelForm):

    class Meta:
        model = models.Tip
        fields = ['content']