import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from duo_auth.models import VerificationDetails

class auth_backend(ModelBackend):
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None, passcode=None):
        try:
            user = User.objects.get(username=username) 
        except User.DoesNotExist:
            return None
        if not user.check_password(password):
            return None
        try:
            verification_details = user.two_factor_details
        except VerificationDetails.DoesNotExist:
            # for users that don't have verification details available
            # log them in regularly
            return user
        if passcode == verification_details.challenge_passcode:
            verification_details.last_verified = datetime.datetime.utcnow()
            verification_details.save()
            return user
        return None




