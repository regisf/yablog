# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'contact/send/$', 'yablog.plugins.contact.send', name="contact_send"),
    
    ## INSERT HERE
)
