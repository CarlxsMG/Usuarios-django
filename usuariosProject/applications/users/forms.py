# DJango imports
from django import forms
from django.contrib.admin.sites import site

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

    passwordRepeat = forms.CharField(
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
    
    def clean_passwordRepeat(self):
        if self.cleaned_data['password'] != self.cleaned_data['passwordRepeat'] and len(self.cleaned_data['password']) > 5 :
            self.add_error('passwordRepeat', 'Las contraseñas son distintas o la longitud debe superar 5!')