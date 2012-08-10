from publicpages.models import Organization, Sponsor, UserGroup, Payment
from django.contrib import admin


class OrganizationAdmin (admin.ModelAdmin):
    #list_display = ('givenName', 'surName', 'project', 'descr', 'startDate', 'endDate', 'still_in_progress', 'duration')
    #list_filter = ['startDate']
    #search_fields = ['givenName', 'surName', 'project']
    #date_hierarchy = 'startDate'
    pass

class SponsorAdmin (admin.ModelAdmin):
    pass

class UserGroupAdmin (admin.ModelAdmin):
    pass


class PaymentAdmin (admin.ModelAdmin):
    pass


admin.site.register (Organization, OrganizationAdmin)
admin.site.register (Sponsor, SponsorAdmin)
admin.site.register (UserGroup, UserGroupAdmin)
admin.site.register (Payment, PaymentAdmin)

