from django import forms
from django.contrib.auth import get_user_model, authenticate 


class Login(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())

    def clean(self):
        super(Login, self).clean()

        if not authenticate(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password')):
            self.add_error("username", "User does not exists!")
            self.add_error("password", "or password is wrong!")
    
class Register(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())
    confirmation_password = forms.CharField(max_length=64, required=True, widget=forms.PasswordInput())

    def clean(self):
        super(Register, self).clean()

        try:
            get_user_model().objects.get(username=self.cleaned_data.get('username'))
            self.add_error('username', 'The username is already exists!')
        except get_user_model().DoesNotExist:
            pass

        if self.cleaned_data.get('password') != self.cleaned_data.get('confirmation_password'):
            self.add_error('confirmation_password', "The confimations and password did not match!")