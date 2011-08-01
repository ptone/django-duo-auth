from django import forms
from django.contrib.auth.forms import AuthenticationForm

from duo_auth.models import VerificationDetails

class DuoAuthForm(AuthenticationForm):
    passcode = forms.CharField(label="Passcode", required=False)
    passcode_included = forms.CharField(required=False, 
            widget=forms.HiddenInput, initial='no')

    def clean(self):
        # TODO can't really use super, as can't prematurely call authenticate?
        super(DuoAuthForm, self).clean(self)
        if self.cleaned_data.get('passcode_included') == 'yes':
            try:
                user = self.get_user()

                verification = user.two_factor_details
            except VerificationDetails.DoesNotExist:
                # TODO should this be a failing error - it is really just an
                # inconsistancy
                raise forms.ValidationError("Passcode not required for this user")
            if self.cleaned_data.get('passcode') != verification.passcode:
                raise forms.ValidationError("Invalid Passcode")
                # date reset happens in authentication func of backend
        return self.cleaned_data

