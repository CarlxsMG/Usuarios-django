# DJango imports
from django import forms
from django.contrib.auth import authenticate

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


# Form without Model
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'style': 'margin: 10px;',
            }
        )
    )

    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
            }
        )
    )

    def clean(self):

        cleaned_data = super(LoginForm, self).clean()

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')

        return self.cleaned_data

class UpdatePasswordForm(forms.Form):

    password_current = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña actual'
            }
        )
    ) 

    password_new = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Nueva contraseña'
            }
        )
    ) 

class VerificationForm(forms.Form):
    cod_register = forms.CharField(required=True)

    
    def __init__(self, pk, *args, **kwargs):
        self.user_id = pk
        super(VerificationForm, self).__init__(*args, **kwargs)
    

    def clean_cod_register(self):
        codigo = self.cleaned_data['cod_register']

        if len(codigo) == 6:
            # Verificacion con el id del usuario, para ver si los codigos concuerdan
            activo = User.objects.cod_validation(
                self.user_id,
                codigo
            )

            if not activo:
                raise forms.ValidationError('El codigo es incorrecto')
        else:
            raise forms.ValidationError('El codigo es incorrecto')