# -*- coding: utf-8 -*-

import re
import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from appview.models import View

try:
    from ckeditor.fields import HTMLField
except:
    from django.db.models import TextField as HTMLField

from blog import sanitize_name, ping_all

class Author(models.Model):
    """ Base class for authors """
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to=settings.BLOG_CONFIG.Download, null=True)
    
    def __unicode__(self):
        return self.user.get_full_name()
    
    def save(self, *args, **kwargs):
        """ Suppression de l'avatar au cas ou il y en a un """
        if self.pk is not None:
            try:
                Author.object.get(pk=self.pk).image.delete()
            except:
                pass
        super(Author, self).save(*args, **kwargs)
        
    def admin_get_image(self):
        if self.image is not None:
            return '<img src="%s" />' % self.image.url
        return "No Image"
    admin_get_image.short_description = "Image"
    admin_get_image.allow_tags = True
    
    def admin_get_post_count(self):
        return Post.objects.filter(Author=self).count()
    admin_get_post_count.short_description = "Nombre de post"
                
class Post(models.Model):
    """ Base class for blog entry"""
    Author = models.ForeignKey("Author", blank=True)
    CreationDateTime = models.DateTimeField(blank=True, null=True, verbose_name=_("Creation date"), help_text=_("The date creation of this post."))
    Title = models.CharField(max_length=100, help_text=u"Titre du billet")
    Shortcut = models.CharField(max_length=255, help_text=u"Raccourci du titre pour l'URL (rempli automatiquement)", verbose_name=u"Raccourci", blank=True)
    Content = HTMLField(help_text=u"Contenu du billet", default="")
    Categorie = models.ForeignKey('Categorie')
    Tags = models.ManyToManyField('Tag', blank=True, null=True)
    Publish = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-CreationDateTime',]
        
    def __unicode__(self):
        return self.Title
    
    def save(self, *args, **kwargs):
        """ Save """
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
        ping_all()
        
    def admin_get_comments_count(self):
        return Comment.objects.filter(post=self).count()
    admin_get_comments_count.short_description  = "Commentaires"
    
    def admin_get_view_count(self):
        """ Display how time the post have been see """
        return "%d fois" % View.objects.filter(internal_url=self.get_absolute_url).values('pk').count()
    admin_get_view_count.short_description = "Vue"
    
    def get_visible_comments(self):
        """ Retourne les commentaires visibles """
        return Comment.objects.filter(Show=True, post=self)

    def get_visible_comments_count(self):
        """ Retourne le nombre de commentaires visibles """
        return self.Commentaire.filter(Show=True).count()

    def get_invisible_comments_count(self):
        return self.Commentaire.filter(Show=False).count()
        
    def get_absolute_url(self):
        return reverse("blog.views.article_short", args=(self.Shortcut,))
  
class Preference(models.Model):
    Name = models.CharField(max_length=100, help_text=u"Nom du blog")
    SubTitle = models.CharField(max_length=100, help_text=u"Sous titre du blog")
    ShowFullArticle = models.BooleanField(default=True, help_text=u"Montrer l'ensemble de l'article plutot qu'un résumé")
    ArticleSampleLength = models.IntegerField(default=25, help_text=u"Taille des articles à afficher si on ne montre pas l'article complet")
    IndexNbArticle = models.SmallIntegerField(default=5, help_text=u"Nombre d'article en page d'accueil")
    AllowComments = models.BooleanField(default=False, help_text=u"Permet les commentaires")
    MaxLastestDisplayed = models.SmallIntegerField(default=5, help_text=u"Nombre maximum des dernières dépêches affichées.")
    
    def __unicode__(self):
        return "Preferences"
    
class Tag(models.Model):
    Nom = models.CharField(max_length=100)

    def __unicode__(self):
        return self.Nom
    
    def get_articles_count(self):
        return Post.objects.filter(Tags=self).count()
    get_articles_count.short_description = "Nombre d'articles"
    
class Categorie(models.Model):
    Nom = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.Nom
    
    def get_articles_count(self):
        return Post.objects.filter(Categorie=self).count()
    get_articles_count.short_description = "Nombre d'articles"
    
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
        ordering = ('CreationDateTime',)
        
    def __unicode__(self):
        a = "En attente"
        if self.Show:
            a = u"Publié"
        return u'%s (%s)' % (self.Email, a)

    def gravatar(self):
        return hashlib.md5(self.Email).hexdigest()+".png";
        
def convert_time():
    import MySQLdb
    conn = MySQLdb.connect('localhost', 'regisblog', 'regisblog', 'regisblog')
    cursor = conn.cursor()
    cursor.execute("SELECT CreationDate, id FROM blog_post")
    cursor2 = conn.cursor()
    for r in cursor.fetchall():
        cursor2.execute("UPDATE blog_post SET CreationDateTime='%s' WHERE id='%s'" % (str(r[0]), r[1]))    
    print "Done"

def convert_time_2():
    import MySQLdb
    conn = MySQLdb.connect('localhost', 'regisblog', 'regisblog', 'regisblog')
    cursor = conn.cursor()
    cursor.execute("SELECT CreationDateTime, id FROM blog_post")
    cursor2 = conn.cursor()
    for r in cursor.fetchall():
        cursor2.execute("UPDATE blog_post SET CreationDate='%s' WHERE id='%s'" % (str(r[0]), r[1]))    
    print "Done"
