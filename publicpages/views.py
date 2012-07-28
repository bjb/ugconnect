
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User

from publicpages.models import Sponsor, UserGroup
from osf import settings

import datetime

menustatus = {
    'news' : 'inactive',
    'sponsor' : '',
    'exhibitor' : '',
    'whenwhere' : ''
}


def index (request):

    sponsors = Sponsor.objects.all ()
    ugs = UserGroup.objects.all ()

    return render_to_response ('index.html',
                               {
            'sponsors' : sponsors,
            'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))


def sponsorships (request):

    menustatus['sponsor'] = 'selected'

    sponsors = Sponsor.objects.all ()
    ugs = UserGroup.objects.all ()

    return render_to_response ('sponsorships.html',
                               {
            'sponsors' : sponsors,
            'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))

def whenwhere (request):

    menustatus['whenwhere'] = 'selected'

    sponsors = Sponsor.objects.all ()
    ugs = UserGroup.objects.all ()

    return render_to_response ('whenwhere.html',
                               {
            'sponsors' : sponsors,
            'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))

def exhibitors (request):

    menustatus['exhibitor'] = 'selected'

    sponsors = Sponsor.objects.all ()
    ugs = UserGroup.objects.all ()

    return render_to_response ('exhibitors.html',
                               {
            'sponsors' : sponsors,
            'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))
