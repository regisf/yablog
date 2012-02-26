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
A better notification system

(c) FLORET Interactive 2011

"""

import smtplib
from email.mime.text import MIMEText
import os
import datetime

from django import template
from django.http import Http404
from django.conf import settings

from notification.models import *


def notification_send(template_shortcut, dest=None, context=None, account_name=None):
    """ Send an email based on a shortcut """
    pref = None
    if account_name is not None:
        try:
            pref = Preference.objects.get(name=account_name)
        except Exception, e:
            raise Http404()
    
    if pref is None:
        pref = Preference.objects.all()[0]
        
    if dest is None:
        dest = pref.sendmail
        
    notif = Notification(template_shortcut)
    notif.push(dest, context)
    notif.send()

class Notification(object):
    def __init__(self, template_shortcut=None):
        self.notif = []
        self.shortcut = template_shortcut
        self.pref = Preference.objects.filter(default_account=True)[0]
        self.connection = smtplib.SMTP(self.pref.server, int(self.pref.port))
        if not self.pref.anonymous:
            self.connection.login(self.pref.username, self.pref.password)
            
    def __del__(self):
        self.connection.quit()
        
    def push(self, dest, context=None, shortcut=None):
        """ Push notifications in a stack.
        Will be release with notification_send_mass"""
        if shortcut is None:
            shortcut = self.shortcut
        subject, body = self.render_template(self.shortcut, context)
        self.notif.append({
            'subject' : subject,
            'body': body,
            'dest': dest
        })

    def send(self):
        """ Send all mails pushed """
        for notif in self.notif:
            msg = MIMEText(notif['body'].encode('UTF-8'), 'plain', 'UTF-8')
            msg['From'] = self.pref.sendmail
            msg['To'] = notif['dest']
            msg['Subject'] = notif['subject'].encode("UTF-8")
    
            self.connection.sendmail(self.pref.sendmail, [notif['dest'], ], msg.as_string())

    def render_template(self, template_shortcut, context):
        temp = Template.objects.get(shortcut=template_shortcut)
        body = u"%s" % temp.body
        subject = u"%s" % temp.subject
        if context is not None:
            subject = template.Template(subject).render(context)
            body = template.Template(body).render(context)
    
        return subject, body
                    
 
def ajax_log(message):
    """ Write a message for debugging ajax calls """
    message = "%s : %s" % (datetime.datetime.today(), message)
    open(os.path.join(settings.MEDIA_ROOT, "ajax_log.txt"), 'a').write("%s\n" % message)
    if settings.DEBUG and settings.IS_LOCAL:
        print message
    
    #if Preferences.objects.filter(default_account=True)[0].send_to_admin == True:
    #    notification_send()

