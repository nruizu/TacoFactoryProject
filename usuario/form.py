#Autor: Nicolas Ruiz
from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ["username", "email", "numDocumento", "celular", "direccion", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())