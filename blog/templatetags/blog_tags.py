# -*- coding: UTF-8 -*-
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

"""

import re

from django import template

from django.utils.translation import ugettext as _

from yablog.blog.models import Post, Page_translation, PostTranslation, CategoryTrans

register = template.Library()

MONTH = {
     1 : _('January'),
     2 : _('February'),
     3 : _('March'),
     4 : _('April'),
     5 : _('May'),
     6 : _('June'),
     7 : _('July'),
     8 : _('August'),
     9 : _('September'),
    10 : _('October'),
    11 : _('November'),
    12 : _('December'),
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
    
@register.filter
def get_page_title_translated(page, lang):
     try:
          return Page_translation.objects.get(Page=page, Language__Code__startswith=lang).Name
     except:
          pass
     return page.Name

@register.filter
def get_translated_title(title, lang):
     try:
          return PostTranslation.objects.get(Post__Title=title, Language__Code__startswith=lang).Title
     except:
          pass
     return title

@register.filter
def get_translated_content(post,prefered_lang, request=None):
     try:
          content =  PostTranslation.objects.get(Post=post, Language__Code__startswith=prefered_lang).Content
          if re.search(r'{{%.*?%}}|{{{.*?}}}', content) is not None:
               content = content.replace('{{%', '{%').replace('%}}', '%}').replace('{{{', '{{').replace('}}}', '}}')
               content = template.Template(content).render(template.Context())
          return content
     except:
          pass
     return post.Content

@register.filter
def get_translated_category(categ, prefered_lang):
     try:
          return CategoryTrans.objects.get(Category__Nom=categ, Language__Code__startswith=prefered_lang).Name
     except:
          pass
     return categ