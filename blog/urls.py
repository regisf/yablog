# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from blog.rss import BlogFeed

urlpatterns = patterns('blog',
    url(r'^$',                              'views.index',          name="home"),
    url(r'^article/$',                      'views.articles',       name="show_all"),
    url(r'^article/(?P<article_short>.*)',  'views.article_short',  name="show_article"),
    url(r'^comment/(?P<article_id>\d+)/$',  'views.comment',        name="show_comments"),
    url(r'^tag/(?P<tag_id>\d+)/$',          'views.tag',            name="show_by_tag"),
    url(r'^categories/(?P<categ_id>\d+)/$', 'views.categories',     name="show_by_category"),
    url(r'^(?P<year>\d+)/$',                'views.show_by_date',   name="show_by_year"),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', 'views.show_by_date',   name="show_by_month"),
    url(r'^rss/$',                          BlogFeed()),
    url(r'^ajax/getnext/$',                 'ajax.getnext',         name="get_next"),
    url(r'^search/$',                       'views.search',         name="search"),
)
