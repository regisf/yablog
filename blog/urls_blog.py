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

from django.conf.urls.defaults import patterns, url

from .rss import BlogFeed

urlpatterns = patterns('',
    url(r'^$',                              'yablog.blog.views.index',          name="home"),
    url(r'^article/$',                      'yablog.blog.views.articles',       name="show_all"),
    url(r'^article/(?P<article_short>.*?)/', 'yablog.blog.views.article_short',  name="show_article"),
    url(r'^comment/$',                      'yablog.blog.views.comment',        name="show_comments"),
    url(r'^dynamiccomment/$',               'yablog.blog.views.dynamic_comment',name='dynmamic_comment'),

    url(r'^tag/(?P<tag_id>\d+)/$',          'yablog.blog.views.tag',            name="show_by_tag_id"),
    url(r'^tag/(?P<tag_name>.*?)/$',        'yablog.blog.views.tag_name',       name="show_by_tag_name"),
    
    url(r'^categories/(?P<categ_id>\d+)/$', 'yablog.blog.views.categories',         name="show_by_category"),
    url(r'^categories/(?P<categ_name>.*?)/$','yablog.blog.views.categories_name',   name="show_by_category_name"),
    url(r'^(?P<year>\d+)/$',                'yablog.blog.views.show_by_date',       name="show_by_year"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', 'yablog.blog.views.show_by_date',       name="show_by_month"),
    url(r'^rss/$',                           BlogFeed(),                name='rss'),
    url(r'^ajax/getnext/$',                 'yablog.blog.ajax.getnext',             name="get_next"),
    url(r'^search/$',                       'yablog.blog.views.search',             name="search"),
    
    url(r'^mobile/gettitles/$',             'yablog.blog.mobile.get_titles',    name="mobile_get_titles"),
    url(r'^mobile/getpage/$',               'yablog.blog.mobile.get_page',      name="mobile_get_page"),
    url(r'^mobile/getnext/$',               'yablog.blog.mobile.get_next',      name="mobile_get_next"),
    url(r'^mobile/gethistory/$',            'yablog.blog.mobile.get_history',   name="mobile_get_history"),
    url(r'^mobile/search/$',                'yablog.blog.mobile.search',        name="mobile_search"),
    url(r'^mobile/getbytag/$',              'yablog.blog.mobile.get_by_tag',    name="mobile_get_by_tag"),
    url(r'^mobile/getbycateg/$',            'yablog.blog.mobile.get_by_categ',  name="mobile_get_by_categ"),
)
