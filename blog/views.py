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

from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils.html import strip_tags
from django.core.validators import email_re
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site

from notification import notification_send, ajax_log
from blog.models import *
from appview.decorators import view_count


def robot(request):
    """ Return robot.txt """
    return HttpResponse("""User-agent: *\nAllow: *\nSitemap: http://%s/sitemap.xml\n""" % Site.objects.get_current().domain, mimetype="text/plain")
    
def maintenance(request):
    """ When you need to work quietly on your blog. Uncomment urls.py line  """
    return render_to_response("maintenance.html")

@cache_page(60)
@view_count
def index(request):
    """ Page d'accueil du blog """
    return render_to_response(settings.BLOG_CONFIG.Templates.index, RequestContext(request))

# article view is template cached
@view_count
def article_short(request, article_short):
    """ Display a article """
    context = RequestContext(request)
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
    context = RequestContext(request)
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
                    notification_send(settings.BLOG_CONFIG.EmailTemplates.newcomment)
                return HttpResponse(loader.render_to_string(settings.BLOG_CONFIG.Templates.post, context))
    except Exception, e:
        ajax_log("Erreur in comment: %s " % e)

    return HttpResponseRedirect('/')

@cache_page(60)
@view_count
def tag(request, tag_id):
    """ Send all articles with the tag. @todo: replace pk with sanitize_name(tag_name) """
    context = RequestContext(request, {
        'blog_posts' : Post.objects.filter(Tags__pk=tag_id, Publish=True),
        'blog_tag' : Tag.objects.get(pk=tag_id).Nom       
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.tags, context)

@cache_page(60)
@view_count
def categories(request, categ_id):
    """ return all posts within a category @todo: replace categ_id with categ name"""
    context = RequestContext(request, {
        'blog_posts': Post.objects.filter(Categorie__pk=categ_id, Publish=True),
        'blog_categorie': Categorie.objects.get(id=categ_id).Nom
    })
    return render_to_response(settings.BLOG_CONFIG.Templates.categories, context)
    
@cache_page(60)
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
