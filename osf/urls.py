from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.http import HttpResponse
from captcha import urls as captcha_urls
from osf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'publicpages.views.index', name='home'),
    # url(r'^osf/', include('osf.foo.urls')),
    url(r'^publicpages/', include('publicpages.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # captchas
    url(r'^captcha/', include(captcha_urls)),

#    # favicon
#    url (r'^favicon.ico', HttpResponse ( ... what?! ..., content_type="image/x-icon")),
)




if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
