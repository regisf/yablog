# -*- coding: UTF-8 -*-
"""
Tags django pour le capatcha

Utilisation : 
{%load capatcha_tags%}
{%create_capatcha%}
<img src="{{capacha.path}}" />

une variable de session request.session['capatcha'] est mise sur l'objet capatcha défini ci-dessous
par conséquence, l'objet request doit être passé dans la vue
"""

import random
import os
import datetime

from PIL import Image, ImageDraw, ImageFont
from django import template
from django.conf import settings
from capatcha.models import Preference

register = template.Library()

class Capatcha(object):
    def __init__(self, request):        
        try:
            pref = Preference.objects.get(id=1)
        except:
            raise Exception(u"Les préférences ne sont pas renseignées")

        # Remove old capatcha
        now = datetime.datetime.now()
        plus = datetime.timedelta(days=1)
        tempdir = os.path.join(settings.MEDIA_ROOT, settings.CAPATCHA_CONFIG.temp)
        for f in os.listdir(tempdir):
            path = os.path.join(tempdir, f)
            ts = os.stat(path).st_mtime
            if datetime.datetime.fromtimestamp(ts) + plus < now:
                try:
                    os.remove(path)
                except:
                    pass
                
        # Create the new one
        random.seed(os.urandom(10))
        code = ''.join([random.choice(pref.charset) for i in xrange(pref.size)])
        img = Image.open(pref.background.path)
        width, height = img.size
        font = ImageFont.truetype(pref.font.path, 42)
        draw = ImageDraw.Draw(img)
        fwidth, fheight = draw.textsize(code, font=font)
        draw.text(((width - fwidth) / 2, (height - fheight) / 2), code, fill='#000000', font=font)
        imgrelpath = os.path.join(settings.MEDIA_URL, settings.CAPATCHA_CONFIG.temp, '%s.png' % request.session._get_session_key())
        img.save("%s%s" % (settings.PROJECT_PATH, imgrelpath), 'PNG')

        self.key = code
        self.path = imgrelpath
        self.casesensitive = pref.casesensitive

    def isValid(self, value):
        """ Test de la validité du capatcha (appelé depuis la vue) """
        if not self.casesensitive:
            value = value.lower()
            self.key = self.key.lower()
        return self.key == value

class CapatchaNode(template.Node):
    def render(self, context):
        if not context.has_key('request'):
            raise Exception("Il faut l'objet REQUEST")
        context['capatcha'] = Capatcha(context['request']) # Pour la vue
        context['request'].session['capatcha'] = context['capatcha'] # Pour le controler
        return ''

@register.tag
def create_capatcha(parser, token):
    """ Création d'un capatcha (voir __doc__)"""
    return CapatchaNode()

