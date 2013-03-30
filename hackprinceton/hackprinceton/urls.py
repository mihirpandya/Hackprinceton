from django.conf.urls import patterns, include, url
from rdtrpr.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
	url(r'^$', view=welcome, name='hello_page'),
    # Examples:
    # url(r'^$', 'hackprinceton.views.home', name='home'),
    # url(r'^hackprinceton/', include('hackprinceton.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
