# -*- coding: UTF-8 -*-

import re
import datetime
import os
import codecs

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import mark_safe
from django.conf import settings

register = template.Library()

@register.filter
@stringfilter
def format_phone(value):
    """ Format un numéro de téléphone """
    try:
        phone = value.replace(" ",'')
        head = phone[:4]
        after = phone[4:]
        return "%s %s %s %s" % (head, after[:2], after[2:4], after[4:])
    except Exception, e:
        pass
    return value

@register.filter
@stringfilter
def div(value,op):
    try:
        return int(value)/int(op)
    except: # Division / 0
        return "0"

@register.simple_tag
def utils_convert_from_media(value):
    """ Convert a media file (js file) from template to full js file """
    sourcefilename = os.path.join(settings.MEDIA_ROOT, value)
    filecontent = codecs.open(os.path.join(settings.MEDIA_ROOT,value),'r', 'utf-8').read()
    name, ext = os.path.splitext(value)
    nname = "%s_proc%s" % (name, ext)
    newname = os.path.join(settings.MEDIA_ROOT, nname)
    fileurl = "%s%s" % (settings.MEDIA_URL, nname)
    if os.path.exists(newname):
        if os.path.getctime(sourcefilename) > os.path.getctime(newname):
            return  fileurl
    newcontent = template.Template(filecontent).render(template.Context())
#    newcontent = re.sub(r'\s+','', newcontent)
    nfile = codecs.open(newname,"w", 'utf-8')
    nfile.write(newcontent)
    
    return fileurl

@register.tag
def findkeys(parser, token):
    """ recherche de mots clefs dans la value et rempaclement par le tag"""
    name, value, keys, tag = token.split_contents()
    class FindKeys(template.Node):
        def __init__(self, value):
            self.value = value
        def render(self, context):
            value = template.Variable(self.value).resolve(context)
            for key in template.Variable(keys).resolve(context):
                regex = re.compile(key, re.IGNORECASE)
                for found in  regex.findall(value):
                    value = regex.sub(tag[1:-1] % found,value)
            return value
    return FindKeys(value)
    
@register.tag
def display_year_range(parser, token):
    """ Affiche une date de départ et d'arrivée . Utile pour les copyrights """
    name, startyear, separator = token.split_contents()
    class DisplayYearRange(template.Node):
        def render(self, context):
            s_year = int(startyear)
            n_year = datetime.datetime.now().year
            if n_year > s_year:
                return "%d%s%d" % (s_year, eval(separator), n_year)
            return startyear
    return DisplayYearRange()