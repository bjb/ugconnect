from django import template
from publicpages.models import WEEKDAYS, WHICHWEEK

register = template.Library()

@register.filter
def weekday_name(weekday_num):

    return WEEKDAYS[weekday_num]


@register.filter
def ordinal (week_num):
    return WHICHWEEK['%s' % week_num]

