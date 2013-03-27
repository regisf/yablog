# -*- coding: utf-8 -*-
# YaBlog
#  (c) Regis FLORET
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
# DISCLAIMED. IN NO EVENT SHALL Regis FLORET BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Plugin for Contact form

"""
import os
import json

from django.template import Template
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from django.conf import settings

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

class Contact(object):
    def __init__(self, context):
        self.context = context
        self.js = None
        self.templ = None
        
    def install_javascript(self):
        """ Install javascript to handling contact form """
        if self.js is None:
            self.js = open(os.path.join(CURRENT_PATH, 'contact.js'), 'r').read()
        self.js = """<script type="text/javascript">{0}</script>""".format(self.js)
        return self.js
                
    def display_form(self):
        """ Display the contact form """
        if self.templ is None:
            self.templ = open(os.path.join(CURRENT_PATH,"contact.html"), "r").read()
        return Template(self.templ).render(self.context)
    
def create(context):
    """ Create the plugin - Entry Point """
    return Contact(context)

def send(request):
    """ Send an email if the form is complete """
    error = []
    
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        captcha = request.POST.get('captcha')
        message = request.POST.get('message')
            
    if name is None:
        error.append('name')
    
    if email is None:
        error.append("email")
        
    if subject is None:
        error.append("subject")
        
    if message is None:
        error.append("message")
        
    if not request.session['capatcha'].isValid(captcha):
        error.append("captcha")

    data = {
        'error': error
    }

    if not error:
        send_mail("[" + get_current_site(request).name.upper() + " CONTACT]" + subject, message, email, settings.ADMINS,fail_silently=True)
    
    return HttpResponse(json.dumps(data), mimetype="application/json")

