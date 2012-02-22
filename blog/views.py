# -*- coding: utf-8 -*-

from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.html import strip_tags
from django.core.validators import email_re
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.utils.translation import ugettext as _

from notification import notification_send, ajax_log
from blog.models import *
from blog.templatetags.blog_tags import BlogConfig
from appview.decorators import view_count

def createContext(request, d={}):
    """ Simple wait create context variable without using 
    Template Context Processor"""
    d.update({
        'name': request.session.get('nom', ''),
        'email': request.session.get('email', ''),
        'blog': BlogConfig()
    })
    return  RequestContext(request, d)


def robot(request):
    """ Return robot.txt """
    return HttpResponse("""User-agent: *\nAllow: *\nSitemap: http://www.regisblog.fr/sitemap.xml\n""", mimetype="text/plain")
    
def maintenance(request):
    """ When you need to work quietly on your blog. Uncomment urls.py line  """
    return render_to_response("maintenance.html")

@cache_page(60)
@view_count
def index(request):
    """ Page d'accueil du blog """
    return render_to_response(settings.BLOG_CONFIG.Templates.index, createContext(request, {'blog': BlogConfig()}))

# article view is template cached
@view_count
def article_short(request, article_short):
    """ Display a article """
    context = createContext(request)
    post = Post.objects.get(Shortcut=article_short)

    if not request.user.is_authenticated():
        try:
            if not post.id in request.session['article_viewed']:
                request.session['article_viewed'].append(post.id)
        except:
            request.session['article_viewed'] = [post.id,]
        finally:
            post.save()
    
    context['blog_post'] = post

    return render_to_response(settings.BLOG_CONFIG.Templates.post, context)

@cache_page(60)
@view_count
def articles(request):
    """ Show all articles in the blog """
    context = createContext(request)
    return render_to_response(settings.BLOG_CONFIG.Templates.all, context)
    
def comment(request, article_id):
    """ Add a comment """
    try:
        if request.method == 'POST':
            context = RequestContext(request, {'request':request})
            post = request.POST
            context['blog_post'] = Post.objects.get(id=article_id)
            if post.has_key('name') and post.has_key('body') and post.has_key('email'):
                name = strip_tags(post['name'].strip())
                email = strip_tags(post['email'].strip())
                body = strip_tags(post['body'].strip())

                error = False
                if not len(name):
                    context['name_err'] = u"Merci de laisser votre nom"
                    error = True
                if not len(email):
                    context['email_err'] = u"Votre adresse email est vide"
                    error = True
                else:
                    if not email_re.match(email):
                        context['email_err'] = u"Votre email n'est pas valide"
                        error = True

                if not len(body):
                    context['body_err'] = u"Le corps de votre message est vide"
                    error = True

                if not request.session['capatcha'].isValid(post['capatcha']):
                    error = True
                    context['capat_err'] = u"Code et entrée différente"

                if error:
                    context['name'] = name
                    context['email'] = email
                    context['body'] = body
                else:
                    request.session['email'] = email
                    request.session['nom'] = name
                    comment = Comment()
                    comment.Email = email
                    comment.UserName = name
                    comment.Comment = body.replace("\n", "<br/>")
                    comment.IPAddress = request.META['REMOTE_ADDR']
                    comment.post = context['blog_post']
                    comment.save()
                    context['merci'] = True
                    notification_send('newcomment')
                return HttpResponse(loader.render_to_string(settings.BLOG_CONFIG.Templates.post, context))
    except Exception, e:
        ajax_log("Erreur in comment: %s " % e)

    return HttpResponseRedirect('/')

@cache_page(60)
@view_count
def tag(request, tag_id):
    """ Renvoi tous les articles ayant un tag : tag_id (m'enfin je me conprends)"""
    context = createContext(request, {
        'blog_posts' : Post.objects.filter(Tags__pk=tag_id, Publish=True),
        'blog_tag' : Tag.objects.get(pk=tag_id).Nom       
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.tags, context)

@cache_page(60)
@view_count
def categories(request, categ_id):
    """ Renvoi tous les articles appartenant à une catégorie """
    context = createContext(request, {
        'blog_posts': Post.objects.filter(Categorie__pk=categ_id, Publish=True),
        'blog_categorie': Categorie.objects.get(id=categ_id).Nom
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.categories, context)
    
@cache_page(60)
@view_count
def show_by_date(request, year, month=None):
    query = Q(Publish=True) & Q(CreationDateTime__year=year)
    if month is not None:
        query &= Q(CreationDateTime__month=month)
    context = createContext(request, {
        'blog_post': Post.objects.filter(query)
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.year, context)

#@cache_page(60)
#@view_count
#def show_by_month(request, year, month):
#    context = createContext(request, {
#        'blog_post': Post.objects.filter(CreationDate__year=year, CreationDate__month=month, Publish=True)
#    })
#    return render_to_response(settings.BLOG_CONFIG.Templates.month, context)

def search(request):
    """ Search engine (quite simple) """
    search_str = request.POST['q'].strip()
    if len(search_str) > 2:
        keywords = search_str.split(' ')
        query = Q()
        for key in keywords:
            query |= Q(Content__icontains=key)

        p = Post.objects.filter(query & Q(Publish=True))
    else:
        p = []
        keywords = [_("No keyword set") ]
    context = createContext(request, { 'keywords' : keywords, 'post_found': p })
    return render_to_response(settings.BLOG_CONFIG.Templates.search, context)
