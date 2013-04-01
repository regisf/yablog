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
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from .models import (Post, Author, Categorie, Tag,
                     SearchEngine, Comment, Preference,
                     Page, PostTranslation, Language,
                     Page_translation, CategoryTrans)

class _PostTranslationInline(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(_PostTranslationInline, self)._construct_form(i, **kwargs)
        form.empty_permitted = True
        return form
    
class PostTranslationInline(admin.StackedInline):
    model = PostTranslation
    extra = 1
    formset = _PostTranslationInline
    
class PostAdmin(admin.ModelAdmin):
    previous_next_buttons = True
    list_display = ("Title", "admin_get_author", 'CreationDateTime', 'Publish',
                    'admin_get_view_count', 'admin_get_comments_count',
                    'admin_get_page', "EnableComment", "EnableNavigation",
                    'admin_get_flag')
    
    search_fields = ('Content',)
    list_filter = ('Tags', 'Categorie', "Author", 'Publish', 'Page' )
    list_editable =  ('Publish', )
    date_hierarchy = 'CreationDateTime'
    inlines = (PostTranslationInline,)

class PostTranslationAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", )
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('admin_get_image', '__unicode__', 'admin_get_post_count')
    
class _CategoryTranslationInline(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(_CategoryTranslationInline, self)._construct_form(i, **kwargs)
        form.empty_permitted = True
        return form
    
class CategoryTranslationInline(admin.StackedInline):
    model = CategoryTrans
    extra = 1
    formset = _CategoryTranslationInline
    
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'admin_get_icon', 'get_articles_count', 'DisplayInList', )
    list_editable = ('DisplayInList', )
    inlines = (CategoryTranslationInline, )
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'get_articles_count', )
    
class SearchEngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'ping_count')
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'CreationDate', 'UserName', 'Show')
    list_editable = ('Show', )
    date_hierarchy = 'CreationDate'

class PageInlineTranslation(BaseInlineFormSet):
    """ Found on Stackoverflow """
    def _construct_form(self, i, **kwargs):
        form = super(PageInlineTranslation, self)._construct_form(i, **kwargs)
        form.empty_permitted = True
        return form

class PageTranslationInline(admin.TabularInline):
    model = Page_translation
    extra = 1
    formset = PageInlineTranslation
    
class PageAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "Shortcut", "Position", 'Default', )
    inlines = [PageTranslationInline,]
    sortable_field_name = "Position"
    list_editable = ('Position', )
    

admin.site.register(Page, PageAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(CategoryTrans)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Preference)
admin.site.register(SearchEngine, SearchEngineAdmin)
admin.site.register(Language)
admin.site.register(PostTranslation, PostTranslationAdmin)