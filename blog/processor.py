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
from django.contrib.sites.models import Site
from django.conf import settings

HAVE_CACHE = True
try:
    from memcache import Client
except ImportError:
    HAVE_CACHE = False
    
from .models import Preference, Post, Categorie, Page

client = None
if HAVE_CACHE:
    client = Client((settings.CACHES['default']['LOCATION'],), settings.CACHE_DURATION)
    
def cache_me(method):
    def _cache_me(self, *args, **kwargs):
        if client:
            data = client.get(settings.CACHES['default']['KEY_PREFIX'] + method.__name__)
            if data is None:
                try:
                    data = method(self, *args, **kwargs)
                except Exception as e:
                    print e
            return data
    return _cache_me

class BlogConfig(object):
    def __init__(self):
        try:
            self.pref = Preference.objects.get_default()
        except:
            ''' Create default preferences '''
            self.pref = Preference(
                Name=_("Default name (fixme)"),
                Subtitle=_("Default subtitle (changeme)")
            )
            self.pref.save()
            if HAVE_CACHE:
                self.client = Client(settings['CACHE']['default']['LOCATION'])

    @cache_me
    def get_title(self):
        return self.pref.Name
    
    @cache_me
    def get_subtitle(self):
        return self.pref.SubTitle
            
    @cache_me
    def get_last_posts(self):
        return self.get_posts()[:self.pref.MaxLastestDisplayed]
     
    @cache_me
    def get_last_ten_posts(self):
        return self.get_posts()[:self.pref.MaxLatestDisplayed * 2]
         
    @cache_me
    def get_posts(self):
        return Post.objects.filter(Publish=True, Page__Default=True)
            
    @cache_me
    def get_categories(self):
        return list(Categorie.objects.select_related('post__categorie').filter(DisplayInList=True).order_by("Nom"))
  
    @cache_me
    def get_tags(self):
        """ Get all tags
        return a list containing a list
            count : Number of tags for all articles
            slice : For tags cloud (1 to 5)
            tag : the tag itself
        """
        all_ = []; [[all_.append(tag.Nom) for tag in list(a.Tags.all())] for a in list(Post.objects.filter(Publish=True).only('Tags__Nom'))]
        aDict = {}
        for kw in all_:
            if not (kw in aDict):
                aDict[kw] = 0
            aDict[kw ] += 1
        
        maxi = 0
        for a in aDict:
            if aDict[a] > maxi:
                maxi = aDict[a]
        
        mini = maxi
        for a in aDict:
            if aDict[a] < mini:
                mini = aDict[a]
            
        tags = []
        slic = maxi / 5 or 1
        
        for tag in aDict:
            tags.append([aDict[tag], aDict[tag] / slic + 1, tag])
        return tags
         
    @cache_me
    def showFullArticle(self):
        return self.pref.ShowFullArticle
     
    @cache_me
    def articleSampleLength(self):
        return self.pref.ArticleSampleLength
     
    @cache_me
    def maxLatestDisplayed(self):
        return self.pref.MaxLastestDisplayed
     
    @cache_me
    def mobile_get_history(self):
        date_ordered = {}
        date_post = []
        [date_post.append({'year': post.CreationDateTime.year, 'month':post.CreationDateTime.month}) for post in Post.objects.filter(Publish=True).only('CreationDateTime')]

        for dp in date_post:
            if not date_ordered.has_key(dp['year']):
                date_ordered[dp['year']] = {}
                
            if not date_ordered[dp['year']].has_key(dp['month']):
                date_ordered[dp['year']][dp['month']] = 0
            date_ordered[dp['year']][dp['month']] += 1
             
        return date_ordered

    @cache_me
    def get_history(self):
        date = {}
        for post in list(Post.objects.filter(Publish=True).order_by("CreationDateTime").values('CreationDateTime')):
            try:
                if date.has_key(post['CreationDateTime'].year):
                    if not post['CreationDateTime'].month in date[post['CreationDateTime'].year]:
                        date[post['CreationDateTime'].year].append(post['CreationDateTime'].month)
                else:
                    date[post['CreationDateTime'].year] = [post['CreationDateTime'].month]
            except:
                pass
            
        for d in date.keys():
            date[d].sort()
        return date
     
    @cache_me
    def last_modified(self):
        return Post.objects.latest('CreationDateTime').CreationDateTime.strftime("%Y-%m-%d %H:%M:%S")
    
    @cache_me
    def get_pages(self):
        return list(Page.objects.all())
    
    
def blog_init(request):
    ''' Add all needed variable in the context instead using createContext '''
    
    return {
        'blog': BlogConfig(),
        'email': request.session.get('email', ''),
        'name': request.session.get('nom', ''),
    }
blog_init.is_usable = True

def site(request):
    site = Site.objects.get_current()
    return {
       'SITE_URL': site.domain,
       'SITE_NAME': site.name
    }

def local(request):
    return  {
       'IS_LOCAL' : settings.IS_LOCAL
    }

def findlocale(request):
    try:
        return { 'PREFERED_LANG' : request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0][:2] }
    except:
        return { 'PREFERED_LANG' : settings.LANGUAGE_CODE }


