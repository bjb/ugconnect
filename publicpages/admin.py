from publicpages.models import Organization, Sponsor, UserGroup, Payment, Theme, UserProfile, BzflagTeam, UserGroup2
from django.contrib import admin
from django.contrib.admin import SimpleListFilter



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


class HasUserGroupFilter(SimpleListFilter):
    title = 'Has user group'
    parameter_name = ('flag')

    def lookups(self, request, model_admin):
        return (
            ('usergroup', 'with reference'),
            ('no usergroup', 'no reference')
            )

    def queryset(self, request, queryset):
        answer = queryset
        if 'usergroup' == self.value ():
            answer = queryset.filter (usergroup__isnull = False)
        elif 'no usergroup' == self.value ():
            answer = queryset.filter (usergroup__isnull = True)

        return answer


class UserGroup2Admin (admin.ModelAdmin):
    list_filter = (HasUserGroupFilter,)

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
admin.site.register (UserGroup2, UserGroup2Admin)
admin.site.register (Payment, PaymentAdmin)
admin.site.register (Theme, ThemeAdmin)
admin.site.register (UserProfile, UserProfileAdmin)
admin.site.register (BzflagTeam, BzflagTeamAdmin)

