# -*- coding: UTF-8 -*-

#import time

from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

from blog.models import Post, Preference

def getnext(request):
    #time.sleep(2)
    try:
        if request.is_ajax():
            articles = int(request.GET.get("articles"))
            pref = Preference.objects.get(id=1)

            context = RequestContext(request,{
                'blog' : {
                    'get_last_posts' : Post.objects.filter(Publish=True)[articles:articles+5],
                    'showFullArticle' : pref.ShowFullArticle,
                    'articleSampleLength' : pref.ArticleSampleLength
                }
            })
        return HttpResponse(loader.get_template('blog/nextpost.html').render(context))    
    except Exception as e:
        #print e
        pass
    
    return HttpResponseBadRequest("Bad request")