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
Template context processor.
"""

from django.utils.translation import ugettext as _

from .models import *


class BlogConfig(object):
     def __init__(self):
          try:
             self.pref = Preference.objects.all()[0]
          except:
            ''' Create default preferences '''
            self.pref = Preference(
                Name=_("Default name (fixme)"),
                Subtitle=_("Default subtitle (changeme)")
            )
            self.pref.save()

         
     def get_title(self):
          return self.pref.Name
     
     def get_subtitle(self):
        return self.pref.SubTitle
        
     def get_last_posts(self):
          return self.get_posts()[:self.maxLatestDisplayed()]
         
     def get_posts(self):
          return Post.objects.filter(Publish=True)
              
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
          if slice == 0:
               slice = 1   # Avoid / 0 for small amount of tags
          
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
    
def blog_init(request):
    ''' Add all needed variable in the context instead using createContext '''
    
    return {
        'blog': BlogConfig(),
        'email': request.session.get('email', ''),
        'name': request.session.get('nom', '')
    }
blog_init.is_usable = True
