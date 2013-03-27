# -*- coding: UTF-8 -*-

import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.template.defaultfilters import truncatewords_html, striptags, date
from django.db.models import Q

from .models import Post, Tag, Categorie
from yablog.appview.decorators import view_count
from yablog.notification import ajax_log
from .templatetags.blog_tags import MONTH

def _convert_to_dict(post):
    return {
        'Title': post.Title,
        'Shortcut': post.Shortcut,
        'Repr' : truncatewords_html(striptags(post.Content), 20),
        'CreationDateTime': date(post.CreationDateTime, "j F Y")
    }

def _get_posts(start, end):
    posts = []
    for post in Post.objects.filter(Publish=True).only('Shortcut', 'Title', 'CreationDateTime', 'Content')[start:end]:
        posts.append(_convert_to_dict(post))
    return json.dumps(posts, ensure_ascii=False)

@view_count
def get_titles(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            posts = _get_posts(0, 10)
            return HttpResponse(posts, mimetype="application/json")
    except Exception as e:
        ajax_log("blog.mobile.get_titles: %s" % e)
        
    return HttpResponseBadRequest('')

@view_count
def get_page(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            shortcut = request.GET['shortcut']
            post = Post.objects.get(Shortcut=shortcut, Publish=True)
            jpost = {
                'Title' : post.Title,
                'Content': post.Content,
                'CreationDateTime': date(post.CreationDateTime, "j F Y")
            }
            return HttpResponse(json.dumps(jpost, ensure_ascii=False), mimetype="application/json")
    except Exception as e:
        ajax_log("blog.mobile.get_page: %s" % e)
        
    return HttpResponseBadRequest('')

def get_next(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            count = int(request.GET['count'])
            posts = _get_posts(count, count+10)
            return HttpResponse(posts, mimetype="application/json")
    except Exception as e:
        ajax_log("blog.mobile.get_next: %s" % e)
        
    return HttpResponseBadRequest('')

def get_history(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            year,month = request.GET['year'].split('-')
            posts = []
            for post in Post.objects.filter(CreationDateTime__year=year, CreationDateTime__month=month, Publish=True).only('CreationDateTime', 'Title', 'Shortcut', 'Content'):
                posts.append(_convert_to_dict(post))
            
            result = {
                'titles' : posts,
                'month' : MONTH[int(month)],
                'year' : year
            }
            return HttpResponse(json.dumps(result, ensure_ascii=False), mimetype="application/json")
    except Exception as e:
        ajax_log("blog.mobile.get_history: %s" % e)
        
    return HttpResponseBadRequest('')
            
def search(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            search_str = request.GET['keyword']
            if len(search_str) >= 3:
                keywords = search_str.split(' ')
                query = Q()
                for key in keywords:
                    query |= Q(Content__icontains=key)

                posts = []
                for post in Post.objects.filter(query & Q(Publish=True)).only('CreationDateTime', 'Title', 'Shortcut', 'Content'):
                    posts.append(_convert_to_dict(post))
                
                return HttpResponse(json.dumps({
                    'titles' : posts,
                    'keywords' : keywords}), mimetype="application/json")
        
    except Exception as e:
        ajax_log("blog.mobile.search : %s" %e)
        
    return HttpResponseBadRequest('')

def get_by_tag(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            tag = Tag.objects.get(Nom=request.GET['tag'])
            posts = []
            [ posts.append(_convert_to_dict(post)) for post in Post.objects.filter(Publish=True, Tags=tag) ]
            return HttpResponse(json.dumps({
                'titles' : posts,
                'tag': tag.Nom
            }), mimetype="application/json")
            
    except Exception as e:
        ajax_log("blog.mobile.get_by_tag: %s " % e)
    return HttpResponseBadRequest('')

def get_by_categ(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            categ = Categorie.objects.get(Nom=request.GET['categ'])
            posts = []
            [ posts.append(_convert_to_dict(post)) for post in Post.objects.filter(Publish=True, Categorie=categ).only('CreationDateTime', 'Title', 'Shortcut', 'Content') ]
            return HttpResponse(json.dumps({
                'titles' : posts,
                'categ': categ.Nom
            }), mimetype="application/json")
            
    except Exception as e:
        ajax_log("blog.mobile.get_by_tag: %s " % e)
    return HttpResponseBadRequest('')