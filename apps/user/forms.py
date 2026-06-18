from django import forms
from .models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# forms.py

class iniciarSesionForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        max_length=150
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput()
    )