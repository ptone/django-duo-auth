from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from duo_auth.models import VerificationDetails

class DuoAuthForm(AuthenticationForm):
    passcode = forms.CharField(label="Passcode", required=False)
    passcode_included = forms.CharField(required=False,
            widget=forms.HiddenInput, initial='no')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        passcode = self.cleaned_data.get('passcode')

        if username and password:
            if self.cleaned_data.get('passcode_included') == 'yes':
                self.user_cache = authenticate(
                        username=username,
                        password=password,
                        passcode=passcode)
            else:
                self.user_cache = authenticate(
                        username=username,
                        password=password)
            if self.user_cache is None:
                # TODO add in note if passcode was required
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data

