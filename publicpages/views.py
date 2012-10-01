
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User

from publicpages.models import Sponsor, UserGroup, Organization, Theme
from publicpages.forms import SponsorForm, UserGroupForm, UserProfileForm
from osf import settings

import datetime
import logging



'''
menustatus can be empty, inactive or selected

inactive means this is not a menu item - never link
active means this page is currently selected
empty means this is a menu item, but not currently selected
'''
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

def theme_init (request):
    themeName = 'UGC2013_triangle'
    theme = Theme.objects.get (name = themeName)

    return (themeName)



def index (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    sorted_sponsors = Sponsor.the_sponsors ()

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('index.html',
                               {
            'sorted_sponsors' : sorted_sponsors,
            'settings' : settings,
            'menustatus' : menustatus,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))


def sponsorships (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['sponsor'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()
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

    theme = Theme.objects.get (name = themeName)

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
            'theme' : theme,
            },
                               context_instance = RequestContext (request))

def whenwhere (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['whenwhere'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('whenwhere.html',
                               {
            'sorted_sponsors' : sorted_sponsors,
            'settings' : settings,
            'menustatus' : menustatus,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))

def exhibitors (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['exhibitor'] = 'selected'

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

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('exhibitors.html',
                               {
            'sorted_sponsors' : sorted_sponsors,
            'ugs' : ugs,
            'extra_form_fields' : extra_form_fields,
            'settings' : settings,
            'menustatus' : menustatus,
            'form' : ef,
            'message' : message,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))

def contactus (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('contactus.html',
                               {
            #'sponsors' : sponsors,
            'sorted_sponsors' : sorted_sponsors,
            #'ugs' : ugs,
            'settings' : settings,
            'menustatus' : menustatus,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))



def custom_403_view(request):
    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('403.html',
                               {
            'settings' : settings,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))


def custom_404_view(request):
    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('404.html',
                               {
            'settings' : settings,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))


def custom_500_view(request):
    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['contactus'] = 'selected'

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('500.html',
                               {
            'settings' : settings,
            'theme' : theme,
            },
                               context_instance = RequestContext (request))
