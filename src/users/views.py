from django.views.generic import *
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import *
from .models import WarehouseUser
from .tokens import user_activation_token


def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = WarehouseUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, WarehouseUser.DoesNotExist):
        user = None
    if user is not None and user_activation_token.check_token(user, token):
        user.active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('about')
    template_name = 'users/login.html'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ActivateEmail(TemplateView):
    template_name = 'users/activate_email_template.html'


class PasswordReActivate(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'password-change'

    def get_redirect_url(self, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uid64']))
            user = WarehouseUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, WarehouseUser.DoesNotExist):
            user = None
        if user is not None and user_activation_token.check_token(user, kwargs['token']):
            kwargs = {'pk': kwargs['uid64']}
        return super().get_redirect_url(*args, **kwargs)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('activate_email')

    def get_form_kwargs(self):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ChangePassword(TemplateView):
    template_name = 'users/password_change_email.html'


class PasswordChangeView(UpdateView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = '/'

    def get_queryset(self):
        id = force_text(urlsafe_base64_decode(self.kwargs['pk']))
        self.kwargs['pk'] = id
        return WarehouseUser.objects.filter(id=id)


class UpdatePassword(FormView):
    form_class = UpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('password-reset-email')

    def get_form_kwargs(self):
        kwargs = super(UpdatePassword, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
