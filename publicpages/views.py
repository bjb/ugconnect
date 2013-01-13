
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User
from django.db.models import Q

from publicpages.models import Sponsor, UserGroup, Organization, Theme, BzflagTeam, UserGroup2
from publicpages.forms import SponsorForm, UserGroupForm, UserProfileForm, BzflagTeamForm, UserGroup2Form
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
    'bzflag' : '',
    'contactus' : '',
    'grouplist' : '',
    'home' : '',
}


def clear_menustatus ():
    for k, v in menustatus.iteritems ():
        menustatus[k] = ''

    menustatus['news'] = 'inactive'

def theme_init (request):
    themeName = 'UGC2013_triangle_whitebg'
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
            'subtitle' : 'User Group Connect',
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
            'subtitle' : 'Sponsors',
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
            'subtitle' : 'Time and Place',
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
            'subtitle' : 'User Groups',
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
            'subtitle' : 'Contact Us',
            },
                               context_instance = RequestContext (request))


def bzflag (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['bzflag'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()
    teams = BzflagTeam.objects.all()
    bftf = None

    match1 = []
    match2 = []
    match3 = []
    match4 = []

    match1_teams = [1, 2,  9, 13]
    match2_teams = [3, 4, 10, 14]
    match3_teams = [5, 6, 11, 15]
    match4_teams = [7, 8, 12, 16]

    count = 0
    if ( 0 < len (teams) ):
        for team in teams:
            count += 1

            if count in match1_teams:
                match1.append (team)
            if count in match2_teams:
                match2.append (team)
            if count in match3_teams:
                match3.append (team)
            if count in match4_teams:
                match4.append (team)

    match1_count = len (match1)
    match2_count = len (match2)
    match3_count = len (match3)
    match4_count = len (match4)

    message = ''

    if 'POST' == request.method:
        bztf = BzflagTeamForm (request.POST)
        if bztf.is_valid ():
            # do this in two stages to get the new team object.
            team = bztf.save ( commit = False)
            team.save ()

            message += 'team %s saved' % bztf.cleaned_data['teamname']
            # clear the form
            bztf = BzflagTeamForm ()
            # add the new team to the appropriate match
            whichmatch = teams.count () + 1
            if whichmatch in match1_teams:
                match1.append (team)
            if whichmatch in match2_teams:
                match2.append (team)
            if whichmatch in match3_teams:
                match3.append (team)
            if whichmatch in match4_teams:
                match4.append (team)
            
    else:
        bztf = BzflagTeamForm ()

    theme = Theme.objects.get (name = themeName)

    return render_to_response ('bzflag.html',
                               {
            'sorted_sponsors' : sorted_sponsors,
            'settings' : settings,
            'menustatus' : menustatus,
            'theme' : theme,
            'form' : bztf,
            'message' : message,
            'match1' : match1,
            'match2' : match2,
            'match3' : match3,
            'match4' : match4,
            'match1_count' : match1_count,
            'match2_count' : match2_count,
            'match3_count' : match3_count,
            'match4_count' : match4_count,
            'subtitle' : 'BZFlag Tournament',
            },
                               context_instance = RequestContext (request))



def grouplist (request):

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['grouplist'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()

    if 'GET' == request.method:
        form = UserGroup2Form ()
        the_ugs = UserGroup2.objects.all ().order_by ('name')
    else:
        form = UserGroup2Form (request.POST)
        if form.is_valid ():
#            sun = form.cleaned_data['show_sunday']
#            mon = form.cleaned_data['show_monday']
#            tue = form.cleaned_data['show_tuesday']
#            wed = form.cleaned_data['show_wednesday']
#            thu = form.cleaned_data['show_thursday']
#            fri = form.cleaned_data['show_friday']
#            sat = form.cleaned_data['show_saturday']
#            ukn = form.cleaned_data['show_unknown']
#
#
#            first = form.cleaned_data['show_first']
#            second = form.cleaned_data['show_second']
#            third = form.cleaned_data['show_third']
#            fourth = form.cleaned_data['show_fourth']
#            fifth = form.cleaned_data['show_fifth']
#            last = form.cleaned_data['show_last']
#            uk2 = form.cleaned_data['show_unknown2']


            whichday = form.cleaned_data['day_of_week']
            if '-1' == whichday:
                the_ugs = UserGroup2.objects.filter (meet_weekday = None).order_by ('name')
            elif '-2' == whichday:
                the_ugs = UserGroup2.objects.all().order_by ('name')
            else:
                the_ugs = UserGroup2.objects.filter (meet_weekday = int (whichday)).order_by ('name')

            whichweek = form.cleaned_data['week_of_month']
            if '-1' == whichweek:
                the_ugs = the_ugs.filter (meet_week_of_month = None).order_by ('name')
            elif '-2' == whichweek:
                the_ugs = the_ugs.order_by ('name')
            else:
                the_ugs = the_ugs.filter (meet_week_of_month = int (whichweek)).order_by ('name')
        else:
            form = UserGroup2Form ()
            the_ugs = UserGroup2.objects.all ().order_by ('name')

    theme = Theme.objects.get (name = themeName)

    return render_to_response (
        'grouplist.html',
        {
            'sorted_sponsors' : sorted_sponsors,
            'settings' : settings,
            'menustatus' : menustatus,
            'the_ugs' : the_ugs,
            'theme' : theme,
            'subtitle' : 'List of Groups in Ottawa',
            'form' : form,
            },
        context_instance = RequestContext (request)
        )


def group (request, id):

    (themeName) = theme_init (request)
    clear_menustatus ()

    sorted_sponsors = Sponsor.the_sponsors ()

    the_ug = UserGroup2.objects.get (pk = int (id))

    theme = Theme.objects.get (name = themeName)

    return render_to_response (
        'group.html',
        {
            'sorted_sponsors' : sorted_sponsors,
            'settings' : settings,
            'menustatus' : menustatus,
            'ug' : the_ug,
            'theme' : theme,
            'subtitle' : 'Group Description',
            },
        context_instance = RequestContext (request)
        )

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
