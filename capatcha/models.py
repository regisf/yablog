# -*- coding: UTF-8 -*-

""" 
Plugin pour les capatachas

(c) FLORET Interactive 2010
"""

from django.db import models
from django.conf import settings

class Preference(models.Model):
    """ Definition des préférences pour le capatcha """
    charset = models.CharField(max_length=100, default="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", help_text="Jeux de caractère utilisé pour générer le capatcha", verbose_name="Jeux de caratères")
    size = models.SmallIntegerField(default=4, help_text=u"Taille par defaut du capatcha", verbose_name="Taille")
    font = models.FileField(upload_to=settings.CAPATCHA_CONFIG.Download, help_text=u"Police de caractère affichée", verbose_name="Police")
    background = models.ImageField(upload_to=settings.CAPATCHA_CONFIG.Download, help_text=u"Image de fond du capatcha", verbose_name="Image de fond")
    casesensitive = models.BooleanField(default=False, help_text=u"Est-ce que le capatcha est sensible aux majuscules et minuscules.", verbose_name=u"Sensible à la casse")

    def __unicode__(self):
        return u"Préférences"
