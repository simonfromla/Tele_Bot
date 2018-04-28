import os
import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from oauth.models import CredentialsModel
from tele_bot import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/calendar.readonly',
    redirect_uri='http://localhost:8000/oauth2callback')


@login_required
def index(request):
    storage = DjangoORMStorage(CredentialsModel,
                               'id',
                               request.user,
                               'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("calendar", "v3", http=http)
        activities = service.calendarList()
        events = service.events()
        # activitylist = activities.list(collection='public',
        #                                userId='me').execute()
        activitylist = activities.list()
        elist = events.list(calendarId="en.south_korea#holiday@group.v.calendar.google.com")
        print(elist)
        print(dir(activitylist))
        print(activitylist.execute())
        # logging.info(activitylist)

        return render(request,
                      'welcome.html',
                      {'activitylist': activitylist.execute(),
                      'events': elist.execute()
                      })


@login_required
def auth_return(request):
    # if not xsrfutil.validate_token(settings.SECRET_KEY,
    #                                request.GET['state'],
    #                                request.user):
    #     return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel,
                               'id',
                               request.user,
                               'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")
