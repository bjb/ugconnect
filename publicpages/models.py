from django.db import models

class Organization(models.Model):
    name = models.CharField (max_length = 64)
    contactname = models.CharField (max_length = 64)
    contactinfo = models.CharField (max_length = 64)
    linkurl = models.CharField (max_length = 128, null = True, blank = True)
    comment = models.TextField (null = True, blank = True)
    howhear = models.TextField (null = True, blank = True)
    # graphic = models.FileField ()
    graphicurl = models.TextField (default = 'images/unknown.png', null = True, blank = True)


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
    organization = models.ForeignKey (Organization)
    mailinglist = models.CharField (max_length = 128, null = True, blank = True)

    def __repr__(self):
        return self.organization.name

    def __unicode__(self):
        return u'%s' % self.__repr__()


