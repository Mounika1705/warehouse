from django.urls import re_path
from .views import ActivateEmail, activate


urlpatterns = [
    re_path(r'activate_email/$', ActivateEmail.as_view(), name="activate_email"),
    re_path(r'activate/(?P<uid64>[0-9A-Za-z_\-]*)/(?P<token>[0-9A-Za-z-]*)/$',
            activate, name='activate')
]