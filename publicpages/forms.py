from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from publicpages.models import Organization, UserGroup, Sponsor, Theme, UserProfile, BzflagTeam, SPONSORCHOICES
from django.contrib.auth.models import User


class OrganizationForm (forms.Form):
    name = forms.CharField (label = 'Organization name:  ',
                            widget = forms.TextInput (attrs={"size" : "64"}),
                            max_length = 64)
    contactname = forms.CharField (label = 'Contact name:  ',
                                   widget = forms.TextInput (attrs={"size" : "64"}),
                                   max_length = 128)
    contactinfo = forms.CharField (label = 'Contact info (phone, email IM):  ',
                                   widget = forms.TextInput (attrs={"size" : "64"}),
                                   max_length = 128)
    linkurl = forms.URLField (label = 'URL for us to link to:  ',
                              widget = forms.TextInput (attrs={"size" : "64"}),
                              max_length = 128, required = False)
    comment = forms.CharField (label = 'Anything else you\'d like to tell us?  ',
                               widget = forms.Textarea (attrs = {'cols' : 60, 'rows' : 6 }),
                               required = False)
    howhear = forms.CharField (label = 'How did you hear about us?  ',
                               widget = forms.Textarea (attrs = {'cols' : 60, 'rows' : 6 }),
                               required = False)
    captcha = CaptchaField ()


    def clean_name (self):
        '''reminder of how it's done'''
        return self.cleaned_data['name']

    def clean_linkurl (self):
        linkurl = self.cleaned_data['linkurl']

        if not linkurl.startswith ('http'):
            linkurl = 'http://' + linkurl

        return linkurl

    def clean (self):
        '''reminder of how it's done'''
        return self.cleaned_data

class SponsorForm (OrganizationForm):

    level = forms.ChoiceField (choices = SPONSORCHOICES)

    def clean_level (self):
        '''reminder of how it's done'''
        return self.cleaned_data ['level']

    def clean (self):
        '''reminder of how it's done'''
        return self.cleaned_data


class UserGroupForm (OrganizationForm):

    mailinglist = forms.EmailField (widget = forms.TextInput (attrs={"size" : "64"}), max_length = 128)

    def clean_mailinglist (self):
        '''reminder of how it's done'''
        return self.cleaned_data['mailinglist']

    def clean (self):
        '''reminder of how it's done'''
        return self.cleaned_data



class UserProfileForm (forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('theme',)


class BzflagTeamForm (forms.ModelForm):
    class Meta:
        model = BzflagTeam
        fields = ('teamname', 'captain', 'navigator', 'weapons_specialist', 'padre', 'contactinfo', 'icon', 'icon_approved', 'score')

    def clean_teamname (self):
        '''
        no duplicate team names
        '''
        cleaned_data = super (BzflagTeamForm, self).clean ()
        tn = cleaned_data.get ('teamname')
        qs = BzflagTeam.objects.filter (teamname__exact = tn)

        if qs.count ():
            raise forms.ValidationError ('Sorry!  Teamname %s already exists; choose another' % self.cleaned_data['teamname'])

        return tn


    def clean (self):
        '''
        max 16 teams
        '''
        cleaned_data = super (BzflagTeamForm, self).clean ()
        qs = BzflagTeam.objects.all ()

        if 16 <= qs.count ():
            raise forms.ValidationError ('Sorry!  Tournament is fully subscribed.  Only 16 teams allowed!')

        return cleaned_data


WEEKDAYS_CHOICES = (
    ('-2', 'All'),
    ('-1', 'Unknown'),
    ( '0', 'Sunday'),
    ( '1', 'Monday'),
    ( '2', 'Tuesday'),
    ( '3', 'Wednesday'),
    ( '4', 'Thursday'),
    ( '5', 'Friday'),
    ( '6', 'Saturday'),
)


WHICHWEEK_CHOICES = (
    ('-2', 'All'),
    ('-1', 'Unknown'),
    ('1', 'First'),
    ('2', 'Second'),
    ('3', 'Third'),
    ('4', 'Fourth'),
    ('5', 'Fifth'),
    ('6', 'Last'),
)

class UserGroup2Form (forms.Form):

    # show_sunday = forms.BooleanField (required = False)
    # show_monday = forms.BooleanField (required = False)
    # show_tuesday = forms.BooleanField (required = False)
    # show_wednesday = forms.BooleanField (required = False)
    # show_thursday = forms.BooleanField (required = False)
    # show_friday = forms.BooleanField (required = False)
    # show_saturday = forms.BooleanField (required = False)
    # show_unknown = forms.BooleanField (required = False)
    # show_all = forms.BooleanField (required = False)
    day_of_week = forms.ChoiceField (choices = WEEKDAYS_CHOICES)


    # show_first = forms.BooleanField (required=False)
    # show_second = forms.BooleanField (required=False)
    # show_third = forms.BooleanField (required=False)
    # show_fourth = forms.BooleanField (required=False)
    # show_fifth = forms.BooleanField (required=False)
    # show_last = forms.BooleanField (required=False)
    # show_unknown2 = forms.BooleanField (required=False)
    # show_all = forms.BooleanField (required=False)
    week_of_month = forms.ChoiceField (choices = WHICHWEEK_CHOICES)

