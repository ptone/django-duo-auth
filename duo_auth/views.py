import datetime

from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings

from twilio.rest import TwilioRestClient

from duo_auth.models import VerificationDetails

twilio_id  = getattr(settings, 'TWILIO_ACCOUT_SID', None)
twilio_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)


def generate_passcode(request):
    def fail():
        return HttpResponse(simplejson.dumps({'passcode_enabled': False}), mimetype='application/json')

    if not request.is_ajax():
        fail()
    if not twilio_id and twilio_token:
        fail()
    if request.method != "GET":
        fail()
    if 'username' not in request.GET:
        fail()
    try:
        user = User.objects.get(username=request.GET['username'])
    except User.DoesNotExist:
        fail()
    try:
        verification_details = user.two_factor_details
    except VerificationDetails.DoesNotExist:
        fail()
    verification_age_limit = getattr(settings, 'PASSCODE_AGE_LIMIT', 30)
    if not verification_details.last_verified + datetime.timedelta(days=verification_age_limit) < datetime.datetime.utcnow():
        fail()
    phone = verification_details.phone
    if phone == "":
        fail()
    passcode_length = getattr(settings, 'PASSCODE_LENGTH', 4)
    verification_details.passcode = User.objects.make_random_password(
            length=passcode_length)
    verification_details.save()
    client = TwilioRestClient(twilio_id, twilio_token)
    # TODO need to check for and use setting: TWILIO_DEFAULT_CALLERID
    message = client.sms.messages.create(to=phone, from_="+15555555555",
        body="your passcode is {0}".format(verification_details.passcode ))
    return HttpResponse(simplejson.dumps({'passcode_enabled': True}), mimetype='application/json')
