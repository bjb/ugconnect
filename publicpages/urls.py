from django.conf.urls import patterns, include, url

urlpatterns = patterns('publicpages.views',
    # Examples:
    # url(r'^$', 'osf.views.home', name='home'),
    # url(r'^osf/', include('osf.foo.urls')),
    url(r'index/$', 'index', name='index'),
    url(r'sponsorships/$', 'sponsorships', name='sponsorships'),
    url(r'usergroups/$', 'exhibitors', name='exhibitors'),
    url(r'whenwhere/$', 'whenwhere', name='whenwhere'),
    url(r'contactus/$', 'contactus', name='contactus'),
    url(r'bzflag/$', 'bzflag', name='bzflag'),
    url(r'grouplist/$', 'grouplist', name='grouplist'),
    url(r'group/(?P<id>\d+)$', 'group', name='group'),
)
