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
from django.db import models

class Preference(models.Model):
    name = models.CharField(max_length=40, help_text=u"Nom du serveur", verbose_name=u"Nom")
    sendmail = models.EmailField(help_text=u"Email par default pour l'envoi d\'email", verbose_name=u"Email")
    anonymous = models.BooleanField(default=False)
    username = models.CharField(blank=True, null=True, max_length=40, help_text=u"Nom d'utilisateur", verbose_name=u"Utilisateur")
    password = models.CharField(blank=True, null=True, max_length=40, help_text=u"Mot de passe", verbose_name="Mot de passe")
    server = models.CharField(max_length=255, help_text=u"Adresse du serveur", verbose_name="Serveur")
    port = models.IntegerField(default=25, help_text=u"Port du serveur")
    default_account = models.BooleanField(default=False, help_text=u"Serveur par défaut", verbose_name=u"Compte par défaut")
    
    def __unicode__(self):
        return self.name
    
    # Admin zone
    def offuscate_pass(self):
        return "*" * len(self.password)
    offuscate_pass.short_description=u"Mot de passe"
    
    def default2string(self):
        if self.default_account:
            return "Oui"
        return "Non"
    default2string.short_description = u"Compte par défaut"
     
class MailingList(models.Model):
    creation = models.DateField(auto_now=True)
    template = models.ForeignKey('Template')
    server = models.ForeignKey('Preference')
    
    def __unicode__(self):
        return "%s : %s" % (self.creation, self.template.resume)
    
class Template(models.Model):
    resume = models.CharField(max_length=255, help_text=u"Résumé du mail", verbose_name=u"Résumé")
    shortcut = models.CharField(max_length=10, help_text=u"Raccourci utilisé en interne", verbose_name="Raccourci")
    subject = models.CharField(max_length=255, help_text="Sujet", verbose_name="Sujet")
    body = models.TextField(help_text="Corps du message", verbose_name="Corps")
    
    def __unicode__(self):
        return self.resume
    


