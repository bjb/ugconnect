from django.db import models
from django.contrib.auth.models import User
from osf.settings import MEDIA_ROOT

from osf import settings

class Organization(models.Model):
    name = models.CharField (max_length = 64)
    contactname = models.CharField (max_length = 64)
    contactinfo = models.CharField (max_length = 64)
    linkurl = models.CharField (max_length = 128, null = True, blank = True)
    comment = models.TextField (null = True, blank = True)
    howhear = models.TextField (null = True, blank = True)
    logo = models.ImageField (upload_to = 'images', default = 'unknown.png')


    def __repr__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.__repr__()


SPONSORCHOICES = (
    ('unknown', 'unknown'),
    ('bronze', 'bronze'),
    ('silver', 'silver'),
    ('gold', 'gold'),
    ('platinum', 'platinum'),
    ('in kind', 'in kind'),
)

class Sponsor (models.Model):
    organization = models.ForeignKey (Organization)
    level = models.CharField (max_length = 16, choices = SPONSORCHOICES, default = 'unknown')
    confirmed = models.BooleanField (default = False)  # only display confirmed sponsors

    def __repr__(self):
        return self.organization.name

    def __unicode__(self):
        return u'%s' % self.__repr__()

    @classmethod
    def sponsors_at_level (kls, lvl):
        return kls.objects.filter (level__exact = lvl, confirmed__exact = True)

    @classmethod
    def the_sponsors (kls):
        '''
        return a list of lists of sponsors - sorted by sponsorship level
        first list = platinum sponsors
        second list = gold
        third = silver; fourth = bronze
        '''
        answer = []

        answer.append (kls.sponsors_at_level ('platinum'))
        answer.append (kls.sponsors_at_level ('gold'))
        answer.append (kls.sponsors_at_level ('silver'))
        answer.append (kls.sponsors_at_level ('bronze'))

        return answer



class Payment (models.Model):
    '''Each time a sponsor gives us money, we record it here.'''
    sponsor = models.ForeignKey (Sponsor)
    amount = models.IntegerField ()  # in cents; Decimal can only be used with python 2.7 and my dev box doesn't have that
    date = models.DateField ()


class UserGroup (models.Model):
    '''
    For the user groups attending this event
    '''
    organization = models.ForeignKey (Organization)
    mailinglist = models.CharField (max_length = 128, null = True, blank = True)
    confirmed = models.BooleanField (default = False)  # only display confirmed UserGroups

    def __repr__(self):
        return self.organization.name

    def __unicode__(self):
        return u'%s' % self.__repr__()


class Theme (models.Model):
    '''
    Some info about the theme
    '''
    name = models.CharField (max_length = 32)
    headergraphic = models.CharField (max_length = 256, null = True, blank = True)
    bullet = models.CharField (max_length = 256, null = True, blank = True)
    favicon = models.CharField (max_length = 256, null = True, blank = True)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.__repr__ ()


class UserProfile (models.Model):
    user = models.ForeignKey (User, unique = True)
    theme = models.ForeignKey (Theme, null = True, blank = True)

    def __repr__(self):
        return self.user.username

    def __unicode__(self):
        return u'%s' % self.__repr__()



class BzflagTeam (models.Model):
    '''
    bzflag team info
    '''
    teamname = models.CharField (max_length = 32)

    captain = models.CharField (max_length = 64)

    navigator = models.CharField (max_length = 64,
                                  blank = True, null = True)

    weapons_specialist = models.CharField (max_length = 64,
                                           blank = True, null = True)

    padre = models.CharField (max_length = 64,
                              blank = True, null = True)

    contactinfo = models.CharField (max_length = 128)

    icon = models.ImageField (upload_to = settings.MEDIA_ROOT,
                              default = 'images/default_bzflag_icon.png')

    icon_approved = models.BooleanField (default = False)

    score = models.IntegerField (default = 0)
    
    def __repr__(self):
        return self.teamname

    def __unicode__(self):
        return u'%s' % self.__repr__()



WEEKDAYS = {
    0 : 'Sunday',
    1 : 'Monday',
    2 : 'Tuesday',
    3 : 'Wednesday',
    4 : 'Thursday',
    5 : 'Friday',
    6 : 'Saturday'
}

WHICHWEEK = {
    '1' : 'first',
    '2' : 'second',
    '3' : 'third',
    '4' : 'fourth',
    '5' : 'fifth',
    '6' : 'last',
    'last' : 'last'
}

def weekday_name(weekday_num):
    return WEEKDAYS[weekday_num]

def ordinal (week_num):
    return WHICHWEEK['%s' % week_num]

class UserGroup2 (models.Model):
    '''
    For the full list of user groups
    '''
    name = models.CharField (max_length = 64)
    meet_weekday = models.IntegerField (WEEKDAYS, blank = True, null = True)
    meet_week_of_month = models.IntegerField (WHICHWEEK, blank = True, null = True)
    meet_description = models.TextField (blank = True, null = True)
    location_name = models.CharField (max_length = 128, blank = True, null = True)
    location_address = models.CharField (max_length = 1024, blank = True, null = True)
    location_note = models.TextField (blank = True, null = True)
    meeting_time = models.TimeField (blank = True, null = True)
    web_site = models.URLField (blank = True, null = True)
    email_site = models.CharField (max_length = 128, blank = True, null = True)
    other_url = models.URLField (blank = True, null = True)

    # in case they are attending - link to the other model
    usergroup = models.ForeignKey (UserGroup, blank = True, null = True)

    def __repr__(self):
        return self.name

    def __unicode__(self):
        return u'%s' % self.__repr__()


    def dump (self):
        answer = ''
        answer += 'Name:\t%s\n' % self.name

        answer += '\tweekday:'
        if self.meet_weekday:
            answer += '\t%s' % WEEKDAYS[self.meet_weekday]
        answer += ('\n')

        answer += '\tweek of month:'
        if self.meet_week_of_month:
            answer += '\t%s' % WHICHWEEK ['%d' % self.meet_week_of_month]
        answer += ('\n')

        answer += '\tmeet_description:'
        if self.meet_description:
            answer += '\t%s' % self.meet_description
        answer += ('\n')

        answer += '\tlocation name:'
        if self.location_name:
            answer += '\t%s\n' % self.location_name
        answer += ('\n')

        answer += '\tlocation address:'
        if self.location_address:
            answer += '\t%s' % self.location_address
        answer += ('\n')

        answer += '\tlocation note:'
        if self.location_note:
            answer += '\t%s' % self.location_note
        answer += ('\n')

        answer += '\tmeeting time:'
        if self.meeting_time:
            answer += '\t%s' % self.meeting_time
        answer += ('\n')

        answer += '\tweb site:'
        if self.web_site:
            answer += '\t%s' % self.web_site
        answer += ('\n')

        answer += '\temail site:'
        if self.email_site:
            answer += '\t%s' % self.email_site
        answer += ('\n')

        answer += '\tother url:'
        if self.other_url:
            answer += '\t%s' % self.other_url
        answer += ('\n')

        answer += ('\n')

        return answer

    def meeting_time_as_string (self):
        answer = ''
        if self.meet_week_of_month:
            answer += 'Meet on the %s ' % ordinal (self.meet_week_of_month)
            if self.meet_weekday:
                answer += '%s ' % weekday_name (self.meet_weekday)
            else:
                answer += 'week '
            answer += 'of each month '
            if self.meeting_time:
                answer += 'at %s' % self.meeting_time.strftime ('%H:%M')
            answer += '.'
        else:
            if self.meet_weekday:
                answer += 'Meet on %s' % weekday_name (self.meet_weekday)
                if self.meeting_time:
                    answer += ' at %s' % self.meeting_time
            else:
                answer += 'Meeting time not known.'

        if self.meet_description:
            answer += '  %s' % self.meet_description

        return answer

    def url_string (self):
        answer = ''

        if self.web_site:
            answer += self.web_site
        elif self.other_url:
            answer = self.other_url

        return answer


    def meeting_location_as_string (self):

        answer = ''

        if self.location_name or self.location_address or self.location_note:
            if self.location_name:
                answer += 'Meetings are at %s.' % self.location_name
            if self.location_address:
                answer += '   Address:  %s.' % self.location_address
            if self.location_note:
                answer += '   Note:  %s.' % self.location_note
        else:
            answer += 'Meeting location not known.'

        return answer
