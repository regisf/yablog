# -*- coding: UTF-8 -*-
# YaBlog
#  (c) Regis FLORET 2012 and later
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Regis FLORET 2012 and later BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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
    
