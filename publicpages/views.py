
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
    'whenwhere' : '',
    'contactus' : '',
}


def clear_menustatus ():
    for k, v in menustatus.iteritems ():
        menustatus[k] = ''

    menustatus['news'] = 'inactive'



def index (request):

    clear_menustatus ()

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

    clear_menustatus ()
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

    clear_menustatus ()
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

    clear_menustatus ()
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

def contactus (request):

    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    sponsors = Sponsor.objects.all ()
    ugs = UserGroup.objects.all ()

    return render_to_response ('contactus.html',
                               {
            'sponsors' : sponsors,
            'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))
