import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from duo_auth.models import VerificationDetails

class auth_backend(ModelBackend):

    def authenticate(self, username=None, password=None, passcode=None):
        user = self.get_user(username)
        if not user:
            return None
        if not user.check_password(password):
            return None
        try:
            verification_details = user.two_factor_details
        except VerificationDetails.DoesNotExist:
            return user
        if passcode == verification_details.challenge_passcode:
            verification_details.last_verified = datetime.datetime.utcnow()
            verification_details.save()
            return user
        return None




