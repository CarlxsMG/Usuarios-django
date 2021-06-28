# DJango imports
from django import forms

# Local models
from .models import User


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
            }
        )
    )

    password_repeat = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña',
            }
        )
    )

    class Meta:
        '''Meta for UserRegisterForm'''

        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'gender',
        )