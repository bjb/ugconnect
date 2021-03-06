
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User
from django.db.models import Q

from publicpages.models import Sponsor, UserGroup, Organization, Theme, BzflagTeam
from publicpages.forms import SponsorForm, UserGroupForm, UserProfileForm, BzflagTeamForm, GroupListForm
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
    ugs = UserGroup.objects.filter (confirmed__exact = True)
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

    debug_str = 'debug_str'

    (themeName) = theme_init (request)
    clear_menustatus ()
    menustatus['grouplist'] = 'selected'

    sorted_sponsors = Sponsor.the_sponsors ()

    if 'GET' == request.method:
        debug_str += '; GET'
        form = GroupListForm ()
        the_ugs = UserGroup.objects.all ().order_by ('organization__name')
    else:
        debug_str += '; not GET'
        form = GroupListForm (request.POST)
        if form.is_valid ():

            debug_str += '; form valid'
            whichdays = form.cleaned_data['day_of_week']
            whichweeks = form.cleaned_data['week_of_month']

            # make a series of Q objects and use them
            query_days = Q()
            for num in whichdays:
                if '-2' == num:
                    query_days = Q()
                    break
                elif '-1' == num:
                    query_days |= Q(meet_weekday__exact = None)
                else:
                    query_days |= Q(meet_weekday__exact = num)

            query_weeks = Q()
            for num in whichweeks:
                if '-2' == num:
                    query_weeks = Q()
                elif '-1' == num:
                    query_weeks |= Q(meet_week_of_month = None)
                else:
                    query_weeks |= Q(meet_week_of_month = num)

            the_ugs = UserGroup.objects.filter (query_days, query_weeks).order_by ('organization__name')

        else:
            debug_str += '; form INvalid'
            debug_str += ':  NON_FIELD_ERRORS: '
            debug_str += '%s; ' % form.non_field_errors ()
            debug_str += ':  FIELD_ERRORS (day_of_week): '
            for error in form['day_of_week'].errors:
                debug_str += error
            debug_str += ':  FIELD_ERRORS (week_of_month): '
            for error in form['week_of_month'].errors:
                debug_str += error
            form = GroupListForm ()
            the_ugs = UserGroup.objects.all ().order_by ('organization__name')

    theme = Theme.objects.get (name = themeName)

    debug_str += '; ALL DONE.'
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
            'debug_str' : debug_str,
            },
        context_instance = RequestContext (request)
        )


def group (request, id):

    (themeName) = theme_init (request)
    clear_menustatus ()

    sorted_sponsors = Sponsor.the_sponsors ()

    the_ug = UserGroup.objects.get (pk = int (id))

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
