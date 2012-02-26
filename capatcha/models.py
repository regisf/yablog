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
