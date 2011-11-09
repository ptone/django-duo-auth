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

    # if not request.is_ajax():
        # return fail()
    if not (twilio_id and twilio_token):
        return fail()
    if request.method != "GET":
        return fail()
    if 'username' not in request.GET:
        return fail()
    try:
        print request.GET['username']
        submitted_uname = request.GET['username']
        user = User.objects.get(username=submitted_uname)
        print submitted_uname

    except User.DoesNotExist:
        return fail()
    print "have user"
    print user
    try:
        verification_details = user.two_factor_details
    except VerificationDetails.DoesNotExist:
        return fail()
    verification_age_limit = getattr(settings, 'PASSCODE_AGE_LIMIT', 30)
    if not verification_details.last_verified + datetime.timedelta(days=verification_age_limit) < datetime.datetime.utcnow():
        return fail()
    phone = verification_details.phone
    if phone == "":
        return fail()
    passcode_length = getattr(settings, 'PASSCODE_LENGTH', 4)
    verification_details.challenge_passcode = User.objects.make_random_password(
            length=passcode_length)
    print verification_details.challenge_passcode
    print phone
    print verification_details.id

    verification_details.save()
    print 'saved'
    client = TwilioRestClient(twilio_id, twilio_token)
    # TODO need to check for and use setting: TWILIO_DEFAULT_CALLERID
    message = client.sms.messages.create(to=phone, from_="+14155992671",
        body="your passcode is {0}".format(verification_details.challenge_passcode ))
    return HttpResponse(simplejson.dumps({'passcode_enabled': True}), mimetype='application/json')
