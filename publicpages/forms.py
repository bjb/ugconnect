from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField
from publicpages.models import Organization, UserGroup, Sponsor, Theme, UserProfile, SPONSORCHOICES
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
