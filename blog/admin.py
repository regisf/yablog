# -*- coding: utf-8 -*-

from django.contrib import admin
from blog.models import *

class PostAdmin(admin.ModelAdmin):
    list_display=("Title", "Author", 'CreationDateTime', 'Publish','admin_get_view_count', 'admin_get_comments_count')
    search_fields = ('Content',)
    list_filter = ('Tags', 'Categorie',"Author", 'Publish', )
    list_editatble =  ('Publish', )
#    date_hierarchy = ('CreationDateTime',)
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('admin_get_image', '__unicode__', 'admin_get_post_count')
    
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'get_articles_count', )
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'get_articles_count', )
    
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Comment)
admin.site.register(Preference)
