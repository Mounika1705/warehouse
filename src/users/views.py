from django.views.generic import CreateView, FormView, TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from .models import WarehouseUser
from .tokens import user_activation_token


def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = WarehouseUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, WarehouseUser.DoesNotExist):
        user = None
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'users/login.html'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ActivateEmail(TemplateView):
    template_name = 'users/activate_email_template.html'


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('activate_email')

    def get_form_kwargs(self):
        kwargs = super(RegisterView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
