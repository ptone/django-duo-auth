from django.db import models
from django.contrib.auth.models import User

class VerificationDetails(models.Model):
    """
    This model stores a small set of data needed to conduct the 2 factor
    authentication
    """
    user = models.OneToOneField(User, related_name='two_factor_details')
    phone = models.TextField(blank=True)
    last_verified = models.DateTimeField(blank=True, null=True)
    enabled = models.BooleanField(default=True)
    challenge_passcode = models.TextField(blank=True)

