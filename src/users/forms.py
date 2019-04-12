from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import user_activation_token
from .models import WarehouseUser
from datetime import date


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        query = User.objects.filter(email=email)
        if query.exists():
            not_active = query.filter(is_active=False)
            if not_active.exists():
                raise forms.ValidationError("User Account is not active. Please Active")
        user = authenticate(request, username=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid Username or Password")
        login(request, user)
        return data


class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    staff = forms.BooleanField(required=False)
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput(attrs={'placeholder': 'ReEnter Password'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = WarehouseUser
        fields = ('first_name', 'last_name', 'email', 'date_of_birth',
                  'gender', 'phone_number', 'employee_id')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Your First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Your Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Example@mail.com'}),
            'date_of_birth': forms.SelectDateWidget(years=[x for x in range(date.today().year - 17, 1940, -1)]),
            'gender': forms.RadioSelect(),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
    #
    # def clean(self, *args, **kwargs):
    #     data = self.cleaned_data
    #     first_name = data.get('first_name')
    #     if not first_name:
    #         raise forms.ValidationError("First Name is required")
    #     return data

    def clean_password2(self):
        """Check that two passwords match"""
        print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True):
        # Save provided password in hashed format
        print("hl")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.staff = self.cleaned_data['staff']
        user.active = False
        print(dir(self))
        current_site = get_current_site(self.request)
        mail_subject = 'Activate Warehouse User Account'
        message = render_to_string('users/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':  urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': user_activation_token.make_token(user)
        })
        to_email = self.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        print('SENT')
        if commit:
            user.save()
        return user


class WarehouseUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = WarehouseUser
        fields = ('first_name', 'last_name', 'date_of_birth', 'email',
                  'gender', 'phone_number', 'staff', 'employee_id')

    def clean_password(self):
        """ Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value."""
        return self.initial['password']
