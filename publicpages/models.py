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


SPONSORCHOICES = (
    ('unknown', 'unknown'),
    ('bronze', 'bronze'),
    ('silver', 'silver'),
    ('gold', 'gold'),
    ('platinum', 'platinum'),
)

class Sponsor (models.Model):
    organization = models.ForeignKey (Organization)
    level = models.CharField (max_length = 16, choices = SPONSORCHOICES, default = 'unknown')


class UserGroup (models.Model):
    organization = models.ForeignKey (Organization)
    mailinglist = models.CharField (max_length = 128, null = True, blank = True)


