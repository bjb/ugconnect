
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User

from publicpages.models import Sponsor, UserGroup, Organization
from publicpages.forms import SponsorForm, UserGroupForm
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

    #sponsors = Sponsor.objects.all ()
    sorted_sponsors = Sponsor.the_sponsors ()
    #ugs = UserGroup.objects.all ()

    return render_to_response ('index.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            #'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))


def sponsorships (request):

    clear_menustatus ()
    menustatus['sponsor'] = 'selected'

    #sponsors = Sponsor.objects.all ()
    sorted_sponsors = Sponsor.the_sponsors ()
    #ugs = UserGroup.objects.all ()
    extra_form_fields = '_sponsor_extra_fields.html'

    sf = None
    message = ''

    if 'POST' == request.method:
        sf = SponsorForm (request.POST)
        if sf.is_valid ():
            theOrgQs = Organization.objects.filter (name__exact = sf.cleaned_data['name'])
            if 0 < theOrgQs.count ():
                theOrg = theOrgQs[0]
            else:
                theOrg = Organization (name = sf.cleaned_data['name'],
                                       contactname = sf.cleaned_data['contactname'],
                                       contactinfo = sf.cleaned_data['contactinfo'])
            if sf.cleaned_data['linkurl']:
                theOrg.linkurl = sf.cleaned_data['linkurl']
            #if sf.cleaned_data['graphicurl']:
            #    theOrg.graphicurl = sf.cleaned_data['graphicurl']
            if sf.cleaned_data['comment']:
                theOrg.comment = sf.cleaned_data['comment']
            if sf.cleaned_data['howhear']:
                theOrg.howhear = sf.cleaned_data['howhear']
            theOrg.save ()
            theSponsor = Sponsor (organization = theOrg,
                                  level = sf.cleaned_data['level'],
                                  confirmed = False)
            theSponsor.save ()

            sf = SponsorForm ()
            message = 'Thank you!  We\'ll get in touch soon with %s to confirm %s\'s sponsorship.' % (theOrg.contactname, theOrg.name)
    else:
        sf = SponsorForm ()

    return render_to_response ('sponsorships.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            #'ugs' : ugs,
            'extra_form_fields' : extra_form_fields,
            'settings' : settings,
            'menustatus' : menustatus,
            'form' : sf,
            'message' : message,
            },
                               context_instance = RequestContext (request))

def whenwhere (request):

    clear_menustatus ()
    menustatus['whenwhere'] = 'selected'

    #sponsors = Sponsor.objects.all ()
    sorted_sponsors = Sponsor.the_sponsors ()
    #ugs = UserGroup.objects.all ()

    return render_to_response ('whenwhere.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            #'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))

def exhibitors (request):

    clear_menustatus ()
    menustatus['exhibitor'] = 'selected'

    #sponsors = Sponsor.objects.all ()
    sorted_sponsors = Sponsor.the_sponsors ()
    ugs = UserGroup.objects.filter (confirmed = True)
    extra_form_fields = '_exhibitor_extra_fields.html'

    ef = None
    message = ''

    if 'POST' == request.method:
        ef = UserGroupForm (request.POST)
        if ef.is_valid ():
            theOrgQs = Organization.objects.filter (name__exact = ef.cleaned_data ['name'])
            if 0 < theOrgQs.count ():
                theOrg = theOrgQs[0]
            else:
                theOrg = Organization (name = ef.cleaned_data['name'],
                                       contactname = ef.cleaned_data['contactname'],
                                       contactinfo = ef.cleaned_data['contactinfo'])
            if ef.cleaned_data['linkurl']:
                theOrg.linkurl = ef.cleaned_data['linkurl']
            if ef.cleaned_data['comment']:
                theOrg.comment = ef.cleaned_data['comment']
            if ef.cleaned_data['howhear']:
                theOrg.howhear = ef.cleaned_data['howhear']
            theOrg.save ()
            theExh = UserGroup (organization = theOrg,
                                mailinglist = ef.cleaned_data['mailinglist'],
                                confirmed = False)
            theExh.save ()

            ef = UserGroupForm ()
            message = 'Thank you!  We\'ll get in touch with %s to confirm %s\'s registration.' % (theOrg.contactname, theOrg.name)
    else:
        ef = UserGroupForm ()

    return render_to_response ('exhibitors.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            'ugs' : ugs,
            'extra_form_fields' : extra_form_fields,
            'settings' : settings,
            'menustatus' : menustatus,
            'form' : ef,
            'message' : message
            },
                               context_instance = RequestContext (request))

def contactus (request):

    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    #sponsors = Sponsor.objects.all ()
    sorted_sponsors = Sponsor.the_sponsors ()
    #ugs = UserGroup.objects.all ()

    return render_to_response ('contactus.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            #'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            },
                               context_instance = RequestContext (request))
