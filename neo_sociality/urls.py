# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
# from neo_facebook import views
from neo_core import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'neo_sociality.views.home', name='home'),
    # url(r'^neo_sociality/', include('neo_sociality.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.show_feed, name='show_feed'),
)
