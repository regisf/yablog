# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from blog.models import Post

class BlogFeed(Feed):
    title = u"Le blog de Régis"
    description = u"Je n'ai certes rien à dire, mais je dis quand même"
    link = "/blog/rss/"
    
    def items(self):
        return Post.objects.filter(Publish=True).order_by('-CreationDate')[:5]
    
    def item_link(self, item):
        return "http://www.regisblog.fr/blog/article/%s" % item.Shortcut
    
    def item_title(self, item):
        return item.Title
    
    def item_description(self, item):
        return item.Content
    
    
    