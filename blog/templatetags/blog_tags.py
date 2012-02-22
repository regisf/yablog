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

class BlogConfig(object):
     def __init__(self):
          try:
             self.pref = Preference.objects.all()[0]
          except:
               raise Exception("Blog preferences not set")
         
     def get_title(self):
          return self.pref.Name
     
     def get_last_posts(self):
          return self.get_posts()[:self.maxLatestDisplayed()]
         
     def get_posts(self):
          return Post.objects.filter(Publish=True).order_by("-CreationDateTime","-id")
     
     def get_latest(self):
          return self.get_posts()[:self.maxLatestDisplayed()]
         
     def get_categories(self):
          return Categorie.objects.all()
          
     def _get_min(self, all):
          min = self._get_max(all)
          for t in all:
              count = t.get_articles_count()
              if count < min:
                  min = count
          return min
     
     def _get_max(self, all):
          max = 0
          for t in all:
              count = t.get_articles_count()
              if count > max:
                  max = count
          return max
  
     def get_tags(self):
          """ Get all tags
          return a list containing a list
              count : Number of tags for all articles
              slice : For tags cloud (1 to 5)
              tag : the tag itself
          """
          tags = []
          all = Tag.objects.all()
          min = self._get_min(all)
          max = self._get_max(all)
          slice = max / 5
          
          for tag in Tag.objects.all():
              count = tag.get_articles_count()
              tags.append([count, count / slice + 1, tag])
          return tags
         
     def showFullArticle(self):
          return self.pref.ShowFullArticle
     
     def articleSampleLength(self):
          return self.pref.ArticleSampleLength
     
     def maxLatestDisplayed(self):
          return self.pref.MaxLastestDisplayed
     
     def get_history(self):
          date = {}
          for post in Post.objects.filter(Publish=True).order_by("CreationDateTime").values('CreationDateTime'):
              if date.has_key(post['CreationDateTime'].year):
                  if not post['CreationDateTime'].month in date[post['CreationDateTime'].year]:
                      date[post['CreationDateTime'].year].append(post['CreationDateTime'].month)
              else:
                  date[post['CreationDateTime'].year] = [post['CreationDateTime'].month]
          for d in date.keys():
              date[d].sort()
          return date
     
     def get_all(self):
          return Post.objects.filter(Publish=True)
    
@register.tag
def blog_init(parser, token):
    class BlogInit(template.Node):
        def render(self, context):
            context['blog'] = BlogConfig()
            return ""
    return BlogInit()

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
    
