# DJango imports
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import (
    View,
    CreateView, 
)

from django.views.generic.edit import (
    FormView,
)

# Local forms
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)

# Local models
from .models import User

# Local functions
from .functions import code_generator


# Create your views here.
class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):

        # Generate code validation
        codigo = code_generator()

        new_user = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            gender = form.cleaned_data['gender'],
            cod_register = codigo
        )

        # Send email with code
        mail_subject = 'Confirmacion email'
        message = '<h1>Codigo de verificacion: ' + codigo + '</h1>'

        mail = EmailMessage(mail_subject, message, to=[form.cleaned_data['email'],])
        mail.content_subtype = 'HTML'
        mail.send()

        # Redirect to view verification code
        return HttpResponseRedirect(
            reverse(
                'users_app:user-verification',
                kwargs={'pk':new_user.id}
            )
        )

class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    def form_valid(self, form):

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        login(self.request, user)

        return super(LoginUser, self).form_valid(form)

class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)

        return HttpResponseRedirect(
            reverse(
                'users_app:user-login'
            )
        )

class UpdatePasswordView(LoginRequiredMixin,FormView):
    template_name = 'users/update_pass.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')
    login_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):

        user_current = self.request.user

        user = authenticate(
            username=user_current.username,
            password=form.cleaned_data['password_current']
        )

        if user:
            password_new = form.cleaned_data['password_new']
            user_current.set_password(password_new)
            user_current.save()

        logout(self.request)

        return super(UpdatePasswordView, self).form_valid(form)


class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()

        kwargs.update(
            {
                'pk': self.kwargs['pk'],
            }
        )

        return kwargs

    def form_valid(self, form):

        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active=True
        )

        return super(CodeVerificationView, self).form_valid(form)