# -*- coding: UTF-8 -*-

"""

"""

import re

from django import template
from django.utils.translation import ugettext as _

from blog.models import *

register = template.Library()

MONTH = {
     1 : _(u'janvier'),
     2 : _(u'février'),
     3 : _(u'mars'),
     4 : _(u'avril'),
     5 : _(u'mai'),
     6 : _(u'juin'),
     7 : _(u'juillet'),
     8 : _(u'août'),
     9 : _(u'septembre'),
    10 : _(u'octobre'),
    11 : _(u'novembre'),
    12 : _(u'décembre'),
}

@register.tag
def blog_get_history(p, t):
    class BlogGetHistoryNode(template.Node):
        def render(self, context):
            date = {}
            for post in Post.objects.filter(Publish=True):
                if date.has_key(post.CreationDateTime.year):
                    date[post.CreationDateTime.year] += 1
                else:
                    date[post.CreationDateTime.year] = 1
    
            context['blog_history'] = date
            return ""
    return BlogGetHistoryNode()

@register.tag
def blog_get_history_by_month(parser, token):
    name, year = token.split_contents()
    class BlogGetHistoryByMonthNode(template.Node):
        def render(self, context):
            return ""
    return BlogGetHistoryByMonthNode()

@register.filter
def tostring(value):
    return MONTH[value]
    
@register.filter
def boldize(value, keywords):
    """ Used for the search result. Boldize keywords found """
    v = ''
    for k in keywords:
        # Get Ten words before and after
        valuelow = value.lower()
        curpos = 0
        while valuelow.find(k.lower(), curpos) != -1:
            pos = valuelow.find(k.lower(), curpos)
            start = "...."
            if curpos == 0:
                start = ""
            v += "%s%s...." % (start, value[pos-50:pos+len(k)+50])
            curpos = pos+len(k)
    value = v
    for k in keywords:
        regex = re.compile(r'%s' %k, re.IGNORECASE)
        value = regex.sub('<strong>%s</strong>' % k, value, re.IGNORECASE | re.DOTALL)
    return value
    
