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

import re
import json
import datetime

from django.template import RequestContext, Template
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.utils.html import strip_tags
from django.core.validators import email_re
from django.shortcuts import render_to_response
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse

from yablog.notification import notification_send, ajax_log
from .models import Post, Comment, Preference, Tag, Categorie, Page
from yablog.appview.decorators import view_count
from yablog.capatcha.templatetags.capatcha_tags import Capatcha

def robot(request):
    """ Return robot.txt """
    return HttpResponse("""User-agent: *\nAllow: *\nSitemap: http://%s/sitemap.xml\n""" % Site.objects.get_current().domain, mimetype="text/plain")
    
def maintenance(request):
    """ When you need to work quietly on your blog. Uncomment urls.py line  """
    return render_to_response("maintenance.html")

@view_count
def index(request):
    """ Page d'accueil du blog """
    return render_to_response(settings.BLOG_CONFIG.Templates.index, RequestContext(request))

@view_count
def article_short(request, article_short):
    """ Display a article """
    context = RequestContext(request)
    # Desktop
    context['blog_post'] = Post.objects.get(Shortcut=article_short, Page__Default=True)
    return render_to_response(settings.BLOG_CONFIG.Templates.post, context)

@view_count
def articles(request):
    """ Show all articles in the blog """
    context = RequestContext(request)
    return render_to_response(settings.BLOG_CONFIG.Templates.all, context)
    
def dynamic_comment(request):
    """ Add a comment in ajax way """
    try:
        if request.method == 'POST' and request.is_ajax():
            post = Post.objects.get(pk=request.POST['article_id'])
            if request.user.is_authenticated():
                name = request.user.username
                email = request.user.email
            else:
                name = strip_tags(request.POST['name'].strip())
                email = strip_tags(request.POST['email'].strip())
                request.session['email'] = email
                request.session['nom'] = name
                
            body = request.POST['body']
            comment = Comment(
                Email = email,
                UserName = name,
                Comment = body,
                IPAddress = request.META['REMOTE_ADDR'],
                post = post,
                Show=True
            )
            comment.save()
            try:
                notification_send(settings.BLOG_CONFIG.EmailTemplates.newcomment)
            except:
                pass
            
            # Create the new capatcha
            captcha = Capatcha(request)
            request.esssion['capatcha'] = captcha
            
            data = {
                'comment' : render_to_string(settings.BLOG_CONFIG.Templates.comment, RequestContext(request, { 'blog_post' : post, 'comment': comment})),
                'captcha': captcha.path
            }
            return HttpResponse(json.dumps(data, ensure_asciii=False), mimetype="application/json")

    except Exception as e:
        ajax_log("blog.views.dynamic_comment: %s " % e)
    return HttpResponseBadRequest('')
            
def comment(request):
    """ Add a comment """
    try:
        if request.method == 'POST':
            context = RequestContext(request)
            post = request.POST
            article_id = post['blog']
            context['blog_post'] = Post.objects.get(id=article_id)
            error = False
            
            if request.user.is_authenticated():
                name = request.user.username
                email = request.user.email
                body = post['body']
            else:
                name = strip_tags(post['name'].strip())
                email = strip_tags(post['email'].strip())
                body = strip_tags(post['body'].strip())

                error = False
                if not len(name):
                    context['name_err'] = _("Thanks to leave name")
                    error = True
                if not len(email):
                    context['email_err'] = _("Your email address is empty")
                    error = True
                else:
                    if not email_re.match(email):
                        context['email_err'] = _('Your email address is not a valid one')
                        error = True

                if not len(body):
                    context['body_err'] = _("The message body is empty")
                    error = True

                if not request.session['capatcha'].isValid(post['capatcha']):
                    error = True
                    context['capat_err'] = _("Wrong secure code")

            if error:
                context['name'] = name
                context['email'] = email
                context['body'] = body
                return render_to_response(settings.BLOG_CONFIG.Templates.post, context)
            else:
                request.session['email'] = email
                request.session['nom'] = name
                Comment.objects.create(
                    Email = email,
                    UserName = name,
                    Comment = body.replace("\n", "<br/>"),
                    IPAddress = request.META['REMOTE_ADDR'],
                    post = context['blog_post'],
                    CreationDateTime = datetime.datetime.now(),
                    Show = Preference.objects.immediate_publishing()
                )
                
                
                try:
                    notification_send(settings.BLOG_CONFIG.EmailTemplates.newcomment)
                except:
                    pass
            messages.add_message(request, messages.INFO, "Votre commentaire a &eacute;t&eacute; post&eacute; avec succ&eacute;s")
            return HttpResponseRedirect(reverse('show_article', args=(context['blog_post'].Shortcut,)))
            
    except Exception, e:
        ajax_log("Erreur in comment: %s " % e)

    return HttpResponseRedirect('/')

@view_count
def tag(request, tag_id):
    """ Send all articles with the tag. @todo: replace pk with sanitize_name(tag_name) """
    context = RequestContext(request)
    tag = Tag.objects.get(pk=tag_id).Nom
    
    context.update({
        'blog_posts' : Post.objects.filter(Tags__pk=tag_id, Publish=True),
        'blog_tag' : tag
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.tags, context)

@view_count
def tag_name(request, tag_name):
    """ Return all articles with the tag name """
    context = RequestContext(request)
    tag = Tag.objects.get(Nom=tag_name)
    
   
    context.update({
        'blog_posts' : Post.objects.filter(Tags=tag, Publish=True),
        'blog_tag' : tag
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.tags, context)

def categories(request, categ_id):
    """ return all posts within a category @todo: replace categ_id with categ name"""
    return HttpResponsePermanentRedirect(Categorie.objects.get(id=categ_id).get_absolute_url())

@view_count
def categories_name(request, categ_name):
    """ return all posts within a category """
    context = RequestContext(request, {
        'blog_posts': list(Post.objects.filter(Categorie__Nom=categ_name, Publish=True)),
        'blog_category': Categorie.objects.get(Nom=categ_name).Nom
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.categories, context)

@view_count
def show_by_date(request, year, month=None):
    """ Show by date. This controller is using for both by_month and by_year """
    query = Q(Publish=True) & Q(CreationDateTime__year=year)
    if month is not None:
        query &= Q(CreationDateTime__month=month)
    context = RequestContext(request, {
        'blog_post': Post.objects.filter(query)
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.year, context)


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
    context = RequestContext(request, { 'keywords' : keywords, 'post_found': p })
    return render_to_response(settings.BLOG_CONFIG.Templates.search, context)

@view_count
def page(request, shortcut):
    page = Page.objects.get(Shortcut=shortcut)
    if page.Default == True:
        return HttpResponseRedirect(reverse('home'))
    
    context = RequestContext(request, { 'page' : page })
    if page.Post is not None:
        context['blog_post'] = page.Post
        if re.search(r'{{%.*?%}}|{{{.*?}}}', context['blog_post'].Content) is not None:
            context['blog_post'].Content = context['blog_post'].Content.replace('{{%', '{%').replace('%}}', '%}').replace('{{{', '{{').replace('}}}', '}}')
            context['blog_post'].Content = Template(context['blog_post'].Content).render(RequestContext(request))
        return render_to_response(settings.BLOG_CONFIG.Templates.post, context)
    context['all_posts'] = list(Post.objects.filter(Page=page, Publish=True))
    return render_to_response(settings.BLOG_CONFIG.Templates.pages, context)

@view_count
def page_article(request, shortcut, article_short):
    context = RequestContext(request)
    context['blog_post'] = Post.objects.get(Shortcut=article_short, Page__Shortcut=shortcut)
    return render_to_response(settings.BLOG_CONFIG.Templates.post, context)
