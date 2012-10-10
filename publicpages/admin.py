from publicpages.models import Organization, Sponsor, UserGroup, Payment, Theme, UserProfile, BzflagTeam
from django.contrib import admin


class OrganizationAdmin (admin.ModelAdmin):
    #list_display = ('givenName', 'surName', 'project', 'descr', 'startDate', 'endDate', 'still_in_progress', 'duration')
    #list_filter = ['startDate']
    #search_fields = ['givenName', 'surName', 'project']
    #date_hierarchy = 'startDate'
    pass

class SponsorAdmin (admin.ModelAdmin):
    list_filter = ('confirmed',)

class UserGroupAdmin (admin.ModelAdmin):
    list_filter = ('confirmed',)


class PaymentAdmin (admin.ModelAdmin):
    pass

class ThemeAdmin (admin.ModelAdmin):
    pass

class UserProfileAdmin (admin.ModelAdmin):
    pass

class BzflagTeamAdmin (admin.ModelAdmin):
    pass


admin.site.register (Organization, OrganizationAdmin)
admin.site.register (Sponsor, SponsorAdmin)
admin.site.register (UserGroup, UserGroupAdmin)
admin.site.register (Payment, PaymentAdmin)
admin.site.register (Theme, ThemeAdmin)
admin.site.register (UserProfile, UserProfileAdmin)
admin.site.register (BzflagTeam, BzflagTeamAdmin)

