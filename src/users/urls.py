from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^activate_email/$', ActivateEmail.as_view(), name="activate_email"),
    re_path(r'^password_reset_activate/(?P<uid64>[0-9A-Za-z_\-]*)/(?P<token>[0-9A-Za-z-]*)/$',
            PasswordReActivate.as_view(), name='password_reset_activate'),
    re_path(r'^activate/(?P<uid64>[0-9A-Za-z_\-]*)/(?P<token>[0-9A-Za-z-]*)/$',
            activate, name='activate'),
    re_path(r'^password_reset/', UpdatePassword.as_view(), name="password-reset"),
    re_path(r'^password_reset_email/', ChangePassword.as_view(), name="password-reset-email"),
    re_path(r'^password_change/(?P<pk>[0-9A-Za-z_\-]*)/', PasswordChangeView.as_view(),
            name="password-change")
]
