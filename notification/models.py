# -*- coding: UTF-8 -*-

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
    


