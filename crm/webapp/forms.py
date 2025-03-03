from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# -- register user


class CreateUserForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# Login User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
