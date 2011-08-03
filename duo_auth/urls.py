from django.conf.urls.defaults import *

# URL patterns for duo_auth
from duo_auth.views import generate_passcode

urlpatterns = patterns('',
  # Add url patterns here
  url(r'generate_passcode/$', generate_passcode)
)
