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
Models for the blog core
"""

import hashlib
import threading
import unicodedata
import re

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from yablog.appview.models import View
from yablog.notification import ajax_log

try:
    from ckeditor.fields import HTMLField
except:
    from django.db.models import TextField as HTMLField

from django.contrib.sitemaps import ping_google
   

# Code from internet
def ping_all(sitemap_url='http://www.regisblog.fr/sitemap.xml'):
    """
    @fixme : Change hard coded name to Site domain
    
    Pings the popular search engines, Google, Yahoo, ASK, and
    Bing, to let them know that you have updated your
    site's sitemap. Returns successfully pinged servers.
    
    We start a thread because ping_google is blocking the main thread.
    """
    engines = SearchEngine.objects.filter(active=True).only('name', 'url')
    
    def pa():
        for engine in engines:
            try:
                ping_google(sitemap_url=sitemap_url, ping_url=engine.url)
                pinged = True
            except:
                pinged = False
                
            if pinged:
                engine.ping_count += 1
                engine.save()
    threading.Thread(target=pa).start()
    
def sanitize_name(name):
    """ Ensure to remove all non-alphanum characters """
    name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
    for c in "&\"'()'ç=²¹~#{}[]+°$£^*µ%!§:/;.,?":
        name = name.replace(c,"")            
    name = name.lower().strip()
    name = re.sub("\s","-",re.sub("\s+$","",name))
    return name

class Page_translation(models.Model):
    """
    Page translation for another language
    """
    Page = models.ForeignKey("Page", verbose_name=_("Page"), help_text=_("The page that's translated"))
    Language = models.ForeignKey("Language", verbose_name=_("Language"), help_text=_("The language for the translation"))
    Name = models.CharField(max_length=140, verbose_name=_("Page name"), help_text=_("The translated page name"))
    
    def __unicode__(self):
        return self.Name
    
class Page(models.Model):
    """
    A page is a post container. If the page is the default, the visitor
    will come on this page
    """
    Name = models.CharField(max_length=140, verbose_name=_("Page name"), help_text=_("The page name as displayed"))
    Shortcut = models.SlugField(max_length=140, verbose_name=_("Shortcut"), help_text=_("Page shortcut (slug) displayed in the URL"))
    Default = models.BooleanField(default=False, verbose_name=_("Default page"), help_text=_("Is is page the default page ?"))
    Post = models.ForeignKey("Post", null=True, blank=True, verbose_name=_("Post"), help_text=_("The blog article"))
    Position = models.PositiveSmallIntegerField(default=0, verbose_name=_("Position"), help_text=_("Position in menu"))
    
    class Meta:
        ordering = ['Position', ]
        
    def __unicode__(self):
        return self.Name
    
    def save(self, *args, **kwargs):
        """
        Save the page. If the page is the default, all pages will be reseted to default=False
        """
        if self.Default == True:
            for p in list(Page.objects.filter(Default=True)):
                # There must be only one default page
                p.Default = False
                p.save()
        if self.Shortcut is None:
            self.Shortcut = sanitize_name(self.Name)
        super(Page, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("page", args=(self.Shortcut,))
    
class Author(models.Model):
    """
    Base class for authors
    """
    user = models.ForeignKey(User, verbose_name=_("User"), help_text=_("The author of the post"))
    image = models.ImageField(upload_to=settings.BLOG_CONFIG.Download, null=True, verbose_name=_("Avatar"), help_text=_("The author avatar image"))
    
    def __unicode__(self):
        return self.user.get_full_name()
    
    def save(self, *args, **kwargs):
        """ Remove the avatar if there one yet """
        if self.pk is not None:
            try:
                Author.object.get(pk=self.pk).image.delete()
            except:
                pass
        super(Author, self).save(*args, **kwargs)
        
    def admin_get_image(self):
        """ Display author picture in the administration """
        if self.image is not None:
            return '<img src="%s" />' % self.image.url
        return _("No Image")
    admin_get_image.short_description = _("Image")
    admin_get_image.allow_tags = True
    
    def admin_get_post_count(self):
        """ for admin : return the number of posts for the author """
        return Post.objects.filter(Author=self).count()
    admin_get_post_count.short_description = _("Post count")
        
        
class PostTranslation(models.Model):
    """ This is the post translation """
    Post = models.ForeignKey("Post")
    Title = models.CharField(max_length=100, help_text=_("Post title"), verbose_name=_("Post title"))
    Content = HTMLField(help_text=_("Post content"), verbose_name=_("Content"), default="")
    Language = models.ForeignKey("Language", verbose_name=_("Language"), help_text=_("The translation language"))
    
    def __unicode__(self):
        return self.Title
    
class Post(models.Model):
    """ Base class for blog entry"""
    Author = models.ForeignKey("Author", blank=True, verbose_name=_("Author"), help_text=_("This post author"))
    Page = models.ForeignKey("Page", blank=True, null=True, verbose_name=_("Page"), help_text=_("The page which upon the post is written"))
    CreationDateTime = models.DateTimeField(blank=True, null=True, verbose_name=_("Creation date"), help_text=_("The date creation of this post."))
    Title = models.CharField(max_length=100, verbose_name=_("Title"), help_text=_("Post title"))
    Shortcut = models.CharField(max_length=255, help_text=_(u"Title shortcut for the URL (automaticly)"), verbose_name=_(u"Shortcut"), blank=True)
    Content = HTMLField(default="",help_text=_("Post content"), verbose_name=_("Content"))
    Categorie = models.ForeignKey('Categorie', verbose_name=_("Category"), help_text=_("The category assigned to the post"))
    Tags = models.ManyToManyField('Tag', blank=True, null=True)
    Language = models.ForeignKey("Language", default=settings.LANGUAGE_CODE, verbose_name=_("Language"), help_text=_("In which language the post is written"))
    Publish = models.BooleanField(default=False, verbose_name=("Publish"), help_text=_("Publish the post"))
    EnableComment = models.BooleanField(default=True, help_text=_(u"Enable commentaries"), verbose_name=_("Commentaries"))
    EnableNavigation = models.BooleanField(default=True, help_text=_(u"Enable inline navigation"), verbose_name=_("Navigation"))
    EnableSharing = models.BooleanField(default=True, verbose_name=_("Sharing bar"), help_text=("Shall the share  buttons must be displayed?"))
    
    class Meta:
        ordering = ['-CreationDateTime',]
        
    def __unicode__(self):
        return self.Title
    
    def save(self, *args, **kwargs):
        """ Sanitize and sluggify the tite for the shortcut and ensure the unique name for the post """
        if self.pk is None:
            # Prevent same shortcut
            s = sanitize_name(self.Title)
            count = 1
            while Post.objects.filter(Shortcut=s).values('pk').count() > 0:
                t = "%s-%d"%(self.Title, count)
                s = sanitize_name(t)
                count += 1
            self.Shortcut = s
        super(Post, self).save(*args, **kwargs)
        
        if not settings.IS_LOCAL:
            ping_all()
        
    def admin_get_comments_count(self):
        return Comment.objects.filter(post=self).count()
    admin_get_comments_count.short_description  = _("Commentaries")
    
    def admin_get_view_count(self):
        """ Display how time the post have been see """
        return "%d fois" % View.objects.filter(internal_url=self.get_absolute_url).values('pk').count()
    admin_get_view_count.short_description = _("View count")
    
    def admin_get_page(self):
        """ Display the page name """
        return self.Page.Name
    
    def admin_get_author(self):
        """ DIsplay the author name """
        return self.Author.user.username
    
    def admin_get_flag(self):
        """ Display the language with a flag """
        return '<img src="'+self.Language.Flag.url+'" alt="flag" />'
    admin_get_flag.allow_tags = True
    admin_get_flag.short_description = _("Language")
    
    def get_visible_comments(self):
        """ Return visible comment """
        return list(Comment.objects.filter(Show=True, post=self))

    def get_comments_count(self):
        return Comment.objects.filter(post=self).only('id').count()

    def get_absolute_url(self):
        return reverse("show_article", args=(self.Shortcut,))
    
    def get_related(self):
        """ Return blog post in the same category """
        return list(Post.objects.filter(models.Q(Categorie=self.Categorie) &
                                        ~models.Q(pk=self.pk) & models.Q(Publish=True)))
    
    def next(self):
        """ Get the next post """
        try:
            return Post.objects.filter(pk__lt=self.pk, Publish=True, Page=self.Page)[0]
        except:
            pass
    
    def previous(self):
        """ Get the previous post """
        try:
            return Post.objects.filter(pk__gt=self.pk, Publish=True, Page=self.Page).reverse()[0]
        except:
            pass
    
    def get_translations(self ):
        """
        
        """
        return list(PostTranslation.objects.filter(Post=self))
    
    
class Language(models.Model):
    """
    Language used for the blog.
    """
    Name = models.CharField(max_length=140, verbose_name=_("Language Name"), help_text=_("The language name"))
    Code = models.CharField(max_length=5, verbose_name=_("Language code"), help_text=_("The internationnal code. You should prefer use it in short (eg.: en for en-US, en-EN, en-CA, fr for fr-FR, fr-BE,..."))
    Flag = models.ImageField(upload_to="flags", verbose_name=("Flag"), help_text=_("The flag for the code. See http://"))
    
    def __unicode__(self):
        return self.Code
    
    def get_url(self, ):
        return "?lang={0}".format(self.Code)
    
    
class PreferenceManager(models.Manager):
    """
    Manager for the preferences
    """
    def get_default(self):
        """
        Get default preferences (the first one)
        """
        return self.get_query_set().all()[0]
        
    def get_name(self):
        """
        Get the blog name
        """
        return self.get_query_set().all()[0].Name
    
    def get_subtitle(self):
        """
        Get the blog subtitle
        """
        return self.get_query_set().all()[0].SubTitle
    
    def immediate_publishing(self):
        """
        is comments are published immedialty ?
        """
        return self.get_query_set().all()[0].PublishComment
    
class Preference(models.Model):
    Name = models.CharField(max_length=100, verbose_name=_("Blog name"), help_text=_("The blog name"))
    SubTitle = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Subtitle"), help_text=_("The blog subtitle"))
    ShowFullArticle = models.BooleanField(default=True,  help_text=u"Montrer l'ensemble de l'article plutot qu'un résumé")
    ArticleSampleLength = models.IntegerField(default=25, help_text=u"Taille des articles à afficher si on ne montre pas l'article complet")
    IndexNbArticle = models.SmallIntegerField(default=5, help_text=u"Nombre d'article en page d'accueil")
    AllowComments = models.BooleanField(default=False, help_text=u"Permet les commentaires")
    MaxLastestDisplayed = models.SmallIntegerField(default=5, help_text=u"Nombre maximum des dernières dépêches affichées.")
    PublishComment = models.BooleanField(default=False, help_text=u"Publish comment without waiting moderation")
    DefaultLanguage = models.ForeignKey("Language", verbose_name=_("Default language"), help_text=_("Which is the default langauge of the blog"))
    
    objects = PreferenceManager()
    
    def __unicode__(self):
        return "Preferences"
    
    def save(self, *args, **kwargs):
        super(Preference, self).save(*args, **kwargs)
            
class Tag(models.Model):
    Nom = models.CharField(max_length=100)
        
    def __unicode__(self):
        return self.Nom
    
    def get_articles_count(self):
        return Post.objects.filter(Tags=self, Publish=True).count()
    get_articles_count.short_description = "Nombre d'articles"

class CategoryTrans(models.Model):
    Name = models.CharField(max_length=100, verbose_name=_("Name"), help_text=_("The category name translated"))
    Category = models.ForeignKey("Categorie", verbose_name=_("Category"), help_text=_("The category to translate"))
    Language = models.ForeignKey("Language", verbose_name=_("Language"), help_text=_("The translation language"))
    
    def __unicode__(self):
        return self.Name
    
class Categorie(models.Model):
    Nom = models.CharField(max_length=100, verbose_name=_("Name"), help_text=_("The category name"))
    Icon = models.ImageField(upload_to="icons", null=True, blank=True)
    DisplayInList = models.BooleanField(default=True, help_text=_("Display in the categories list"), verbose_name=_("Display"))
    
    def __unicode__(self):
        return self.Nom
    
    def get_absolute_url(self):
        return reverse('show_by_category_name', args=(self.Nom,))
    
    def get_articles_count(self):
        return Post.objects.filter(Categorie=self).count()
    get_articles_count.short_description = "Nombre d'articles"
    
    def admin_get_icon(self):
        try:
            return '<img src="' + self.Icon.url + '" alt="icon" />'
        except:
            return "No Icon"
    admin_get_icon.short_description = "Icon"
    admin_get_icon.allow_tags = True
    
class Comment(models.Model):
    CreationDate = models.DateField(auto_now=True)
    CreationDateTime = models.DateTimeField(blank=True, null=True)
    UserName = models.CharField(max_length=100)
    Email = models.EmailField()
    IPAddress =  models.IPAddressField()
    Comment = models.TextField()
    Show = models.BooleanField(default=False)
    post = models.ForeignKey('Post', null=True)
    
    class Meta:
        ordering = ('CreationDate',)
        
    def __unicode__(self):
        return self.post.Title

    def gravatar(self):
        return hashlib.md5(self.Email).hexdigest()+".png";
    
class SearchEngine(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    ping_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name
