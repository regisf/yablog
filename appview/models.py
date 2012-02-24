# -*- coding: UTF-8 -*-

"""
AppView
"""

import re
from django.utils.translation import ugettext as _

from django.db import models

class Exclude(models.Model):
    """
    Store exclusion
    """
    name = models.CharField(max_length=140, verbose_name=_("Name"))
    exclude_regex = models.CharField(max_length=140, blank=True, verbose_name=_("Exclude Regex"))
    exclude_IP = models.IPAddressField(blank=True, verbose_name=_("Exclude IP"))
    
    def __unicode__(self):
        return self.name
    
    def match(self, browser):
        """ test if the client is in the exclusion db  """
        return  len(re.findall(self.exclude_regex, browser, re.I)) > 0
        
class View(models.Model):
    last_view = models.DateTimeField()
    ip = models.IPAddressField(blank=True)
    browser = models.CharField(max_length=255)
    internal_url = models.CharField(max_length=255)
    lang = models.CharField(max_length=40)
    session_key = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.ip
    
    def admin_get_browser(self):
        return self.browser[:40]
    admin_get_browser.short_description = u"Browser"
    admin_get_browser.order_admin = 'browser'
    
